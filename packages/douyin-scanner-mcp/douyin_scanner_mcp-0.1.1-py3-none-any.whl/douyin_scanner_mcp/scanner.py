"""
抖音账号扫描器模块
"""
import asyncio
import json
import os
import time
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging
from urllib.parse import urlparse

from playwright.async_api import async_playwright, TimeoutError, Page

from .config import (
    BROWSER_TYPE,
    BROWSER_HEADLESS,
    BROWSER_TIMEOUT,
    DOUYIN_SCAN_MAX_VIDEOS,
    DOUYIN_INJECTION_SCRIPT,
    logger
)

async def scan_douyin_account_page(account_url: str, max_videos: int = None) -> Dict[str, Any]:
    """
    使用 Playwright 扫描抖音账号页面并提取数据
    
    Args:
        account_url: 抖音账号的 URL
        max_videos: 最大扫描视频数量
    
    Returns:
        包含账号信息和视频列表的字典
    """
    if max_videos is None:
        max_videos = DOUYIN_SCAN_MAX_VIDEOS
        
    logger.info(f"开始扫描抖音账号: {account_url}, 最大视频数: {max_videos}")
    
    async with async_playwright() as p:
        browser_type = getattr(p, BROWSER_TYPE)
        browser = await browser_type.launch(headless=BROWSER_HEADLESS)
        
        try:
            context = await browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            
            # 创建页面
            page = await context.new_page()
            
            # 添加路由处理程序，主动拦截API响应
            await context.route('**/aweme/v1/web/aweme/post/**', lambda route: 
                handle_route(route, "video_data"))
            await context.route('**/aweme/v1/web/user/profile/other/**', lambda route: 
                handle_route(route, "profile_data"))
                
            async def handle_route(route, data_type):
                response = await route.fetch()
                json_body = None
                
                try:
                    body = await response.text()
                    json_body = json.loads(body)
                    if data_type == "profile_data":
                        await page.evaluate(f"""
                        window.__interceptedDouyinProfileData = {{
                            url: "{response.url}",
                            status: {response.status},
                            data: {json.dumps(json_body)},
                            timestamp: Date.now(),
                            info: {{ name: "handle_route" }}
                        }};
                        """)
                        logger.info("成功拦截用户资料API")
                    elif data_type == "video_data":
                        # 保存到全局变量
                        await page.evaluate(f"""
                        window.__interceptedDouyinData = {{
                            url: "{response.url}",
                            status: {response.status},
                            data: {json.dumps(json_body)},
                            timestamp: Date.now(),
                            info: {{ name: "handle_route" }}
                        }};

                        // 将每个响应都添加到列表中，用于合并处理
                        if (!window.__interceptedDouyinDataList) {{
                            window.__interceptedDouyinDataList = [];
                        }}
                        
                        const shouldAddToList = {json_body}.data?.aweme_list?.length > 0;
                        if (shouldAddToList) {{
                            window.__interceptedDouyinDataList.push({{
                                url: "{response.url}",
                                status: {response.status},
                                data: {json.dumps(json_body)},
                                timestamp: Date.now(),
                                info: {{ name: "handle_route" }}
                            }});
                        }}
                        """)
                        logger.info("成功拦截视频列表API")
                except Exception as e:
                    logger.error(f"处理API响应时出错: {str(e)}")
                
                await route.fulfill(
                    status=response.status,
                    headers=response.headers,
                    body=await response.body()
                )
            
            # 设置超时
            page.set_default_timeout(BROWSER_TIMEOUT)
            
            # 同时注入脚本以增加兼容性
            await page.add_init_script(DOUYIN_INJECTION_SCRIPT)
            
            # 重试策略
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    logger.info(f"尝试加载页面 (尝试 {retry_count+1}/{max_retries}): {account_url}")
                    # 访问页面
                    await page.goto(account_url, wait_until="domcontentloaded", timeout=60000)
                    break
                except TimeoutError:
                    retry_count += 1
                    if retry_count >= max_retries:
                        logger.warning("页面加载超时，但将继续尝试提取数据")
                    else:
                        logger.warning(f"页面加载超时，重试中 ({retry_count}/{max_retries})")
                        await asyncio.sleep(2)
            
            # 等待页面内容加载
            await asyncio.sleep(3)
            
            # 获取账号视频总数，以便知道需要加载多少视频
            video_count = 0
            try:
                video_count_js = """
                () => {
                    // 尝试从API数据中获取总视频数
                    if (typeof window.__interceptedDouyinProfileData !== 'undefined' && 
                        window.__interceptedDouyinProfileData.data && 
                        window.__interceptedDouyinProfileData.data.user) {
                        return window.__interceptedDouyinProfileData.data.user.aweme_count || 0;
                    }
                    
                    // 如果API数据不可用，尝试从DOM中获取
                    const countText = Array.from(document.querySelectorAll('*')).find(el => 
                        el.textContent && el.textContent.includes('作品') && 
                        /\d+\s*作品/.test(el.textContent)
                    )?.textContent;
                    
                    if (countText) {
                        const match = countText.match(/(\d+)\s*作品/);
                        if (match) return parseInt(match[1]);
                    }
                    
                    return 0;
                }
                """
                video_count = await page.evaluate(video_count_js)
                if video_count > 0:
                    logger.info(f"检测到该账号有 {video_count} 个视频作品")
            except Exception as e:
                logger.warning(f"获取视频总数失败: {str(e)}")
            
            # 动态调整滚动尝试次数
            target_videos = min(max_videos, video_count) if video_count > 0 else max_videos
            max_scroll_attempts = 30 if target_videos > 20 else 10
            logger.info(f"将进行最多 {max_scroll_attempts} 次滚动以加载最多 {target_videos} 个视频")
            
            # 执行增强版页面滚动函数
            enhanced_scroll_js = f"""
            async () => {{
                // 滚动到页面底部以触发更多数据加载
                let lastHeight = 0;
                let currentHeight = document.body.scrollHeight;
                let attempts = 0;
                let maxAttempts = {max_scroll_attempts}; 
                let loadedVideos = 0;
                let previousLoadedVideos = 0;
                let noChangeCount = 0;
                
                // 检查已加载视频数量的函数
                const getLoadedVideosCount = () => {{
                    if (typeof window.__interceptedDouyinDataList !== 'undefined') {{
                        // 计算所有已加载的视频总数
                        let totalVideos = 0;
                        const processedIds = new Set();
                        
                        window.__interceptedDouyinDataList.forEach(data => {{
                            if (data?.data?.aweme_list) {{
                                data.data.aweme_list.forEach(video => {{
                                    if (video.aweme_id && !processedIds.has(video.aweme_id)) {{
                                        processedIds.add(video.aweme_id);
                                        totalVideos++;
                                    }}
                                }});
                            }}
                        }});
                        
                        return totalVideos;
                    }}
                    
                    // 备用方法，数直接通过DOM计数
                    return document.querySelectorAll('a[href*="/video/"]').length;
                }};
                
                console.log("开始滚动页面以加载更多视频...");
                
                // 执行滚动并等待新内容加载
                const scrollAndWait = async () => {{
                    window.scrollTo(0, document.body.scrollHeight);
                    
                    // 尝试点击"加载更多"按钮（如果存在）
                    const loadMoreBtn = Array.from(document.querySelectorAll('button')).find(
                        btn => btn.textContent.includes('加载') || btn.textContent.includes('更多')
                    );
                    if (loadMoreBtn) {{
                        console.log("找到加载更多按钮，尝试点击");
                        loadMoreBtn.click();
                    }}
                    
                    await new Promise(resolve => setTimeout(resolve, 2000)); 
                    return document.body.scrollHeight;
                }};
                
                // 检查是否已加载足够的视频
                const hasLoadedEnoughVideos = () => {{
                    return loadedVideos >= {target_videos};
                }};
                
                // 主循环
                while (attempts < maxAttempts) {{
                    // 检查加载的视频数量
                    loadedVideos = getLoadedVideosCount();
                    console.log(`已加载 ${{loadedVideos}} 个视频，目标: {target_videos}`);
                    
                    // 如果已加载足够的视频，停止滚动
                    if (hasLoadedEnoughVideos()) {{
                        console.log(`已达到目标视频数量 ${{loadedVideos}} >= {target_videos}，停止滚动`);
                        break;
                    }}
                    
                    // 如果视频数量没有变化，增加计数器
                    if (loadedVideos === previousLoadedVideos) {{
                        noChangeCount++;
                        // 如果连续5次滚动后视频数量没有变化，停止滚动
                        if (noChangeCount >= 5) {{
                            console.log(`视频数量连续 ${{noChangeCount}} 次没有变化，停止滚动`);
                            break;
                        }}
                    }} else {{
                        noChangeCount = 0;
                        previousLoadedVideos = loadedVideos;
                    }}
                    
                    // 滚动页面
                    currentHeight = await scrollAndWait();
                    
                    // 如果页面高度没有增加，可能已经到底了
                    if (currentHeight === lastHeight) {{
                        // 额外检查：尝试一次强制滚动，有时加载需要额外操作
                        window.scrollTo(0, 0);
                        await new Promise(resolve => setTimeout(resolve, 1000));
                        window.scrollTo(0, document.body.scrollHeight);
                        await new Promise(resolve => setTimeout(resolve, 2000));
                        
                        currentHeight = document.body.scrollHeight;
                        if (currentHeight === lastHeight) {{
                            console.log("页面高度不再增加，可能已加载全部内容");
                            break;
                        }}
                    }}
                    
                    lastHeight = currentHeight;
                    attempts++;
                }}
                
                return getLoadedVideosCount();
            }};
            """
            
            # 执行滚动脚本
            try:
                loaded_videos_count = await page.evaluate(enhanced_scroll_js)
                logger.info(f"滚动加载完成，实际加载了 {loaded_videos_count} 个视频")
            except Exception as e:
                logger.error(f"执行滚动加载脚本时出错: {str(e)}")
            
            # 等待API数据完全加载（给一些额外时间以确保拦截处理完成）
            await asyncio.sleep(2)
            
            # 检查是否成功获取到API数据
            has_api_data = await wait_for_api_data(page)
            
            # 提取账号数据
            account_data = await extract_account_data(page, account_url)
            
            # 提取视频数据
            videos_data = await extract_video_data(page)
            
            # 限制视频数量
            if max_videos and len(videos_data) > max_videos:
                videos_data = videos_data[:max_videos]
            
            # 构造结果
            result = {
                "success": True,
                "account_data": account_data,
                "videos_data": videos_data,
                "account_url": account_url
            }
            
            logger.info(f"完成扫描账号 {account_url}, 获取了 {len(videos_data)} 个视频")
            
            return result
            
        except Exception as e:
            logger.error(f"扫描账号时出错: {str(e)}")
            # 尝试捕获屏幕截图用于调试
            try:
                if 'page' in locals():
                    screenshot_path = f"error_screenshot_{int(time.time())}.png"
                    await page.screenshot(path=screenshot_path)
                    logger.info(f"错误屏幕截图已保存到: {screenshot_path}")
            except Exception as screenshot_error:
                logger.error(f"尝试保存错误屏幕截图时失败: {str(screenshot_error)}")
                
            raise
        finally:
            await browser.close()


async def load_more_videos(page: Page, max_videos: int) -> None:
    """
    滚动页面加载更多视频
    
    Args:
        page: Playwright 页面对象
        max_videos: 最大视频数量
    """
    logger.info(f"开始滚动加载视频，目标视频数: {max_videos}")
    
    # 初始视频计数
    video_count = 0
    last_video_count = 0
    scroll_count = 0
    max_scroll_attempts = 30  # 最大滚动尝试次数
    no_change_count = 0  # 连续无变化的次数
    
    while True:
        # 检查当前视频数量
        try:
            video_count = await page.evaluate("""() => {
                const videos = document.querySelectorAll('.xg-video-container');
                return videos.length;
            }""")
        except Exception as e:
            logger.warning(f"检查视频数量时出错: {str(e)}")
            video_count = 0
        
        logger.debug(f"当前视频数: {video_count}, 目标视频数: {max_videos}")
        
        # 如果达到目标视频数或者滚动次数过多，停止滚动
        if (video_count >= max_videos) or (scroll_count >= max_scroll_attempts):
            logger.info(f"已达到目标视频数或最大滚动次数，停止滚动。当前视频数: {video_count}")
            break
        
        # 如果视频数量没有变化，增加计数器
        if video_count == last_video_count:
            no_change_count += 1
        else:
            no_change_count = 0
            last_video_count = video_count
        
        # 如果连续5次滚动后视频数量没有变化，停止滚动
        if no_change_count >= 5:
            logger.info(f"视频数量连续 {no_change_count} 次没有变化，停止滚动。当前视频数: {video_count}")
            break
        
        # 滚动页面
        await page.evaluate("window.scrollBy(0, 1000)")
        await asyncio.sleep(1)  # 等待内容加载
        scroll_count += 1


async def wait_for_api_data(page: Page) -> bool:
    """
    等待API数据加载
    
    Args:
        page: Playwright 页面对象
        
    Returns:
        是否成功获取到API数据
    """
    logger.info("等待API数据加载...")
    
    max_attempts = 10
    for attempt in range(max_attempts):
        check_result = await page.evaluate("""() => {
            if (typeof window.checkInterceptedData === 'function') {
                return window.checkInterceptedData();
            }
            return { hasProfileData: false, hasVideoData: false };
        }""")
        
        logger.debug(f"数据检查结果: {check_result}")
        
        if check_result.get('hasProfileData') or check_result.get('hasVideoData') or check_result.get('hasMultipleData'):
            logger.info(f"成功获取API数据，尝试次数: {attempt + 1}")
            return True
        
        await asyncio.sleep(1)
    
    logger.warning(f"等待API数据超时，将尝试从DOM中提取数据")
    return False


async def extract_account_data(page: Page, account_url: str) -> Dict[str, Any]:
    """
    从页面中提取账号数据
    
    Args:
        page: Playwright 页面对象
        account_url: 抖音账号的 URL
        
    Returns:
        包含账号信息的字典
    """
    logger.info("正在提取账号数据...")
    
    # 获取用户ID和secUID
    user_id = ""
    sec_uid = ""
    try:
        # 使用 Python 的 URL 解析
        parsed_url = urlparse(account_url)
        path_parts = parsed_url.path.split('/')
        if len(path_parts) > 0:
            user_id = path_parts[-1]
        
        # 如果有查询参数，尝试提取 sec_uid
        query_params = parsed_url.query.split('&')
        for param in query_params:
            if param.startswith('sec_uid='):
                sec_uid = param.split('=')[1]
                break
    except Exception as e:
        logger.warning(f"从URL提取用户ID时出错: {str(e)}")
    
    # 优先从API数据中提取
    profile_js = """
    () => {
        if (window.__interceptedDouyinProfileData && 
            window.__interceptedDouyinProfileData.data && 
            window.__interceptedDouyinProfileData.data.user) {
            return window.__interceptedDouyinProfileData.data;
        }
        return null;
    }
    """
    
    try:
        profile_data = await page.evaluate(profile_js)
        
        if profile_data and 'user' in profile_data:
            user_info = profile_data['user']
            
            # 处理用户数据
            account_data = {
                "nickname": user_info.get('nickname', ''),
                "signature": user_info.get('signature', ''),
                "follower_count": user_info.get('follower_count', 0),
                "following_count": user_info.get('following_count', 0),
                "likes_received": user_info.get('total_favorited', 0),
                "verified": user_info.get('custom_verify', '') != '',
                "account_url": account_url,
                "unique_id": user_info.get('unique_id', ''),
                "sec_uid": user_info.get('sec_uid', sec_uid),
                "account_type": user_info.get('account_type', 0),
                "avatar_url": user_info.get('avatar_larger', {}).get('url_list', [''])[0],
                "video_count": user_info.get('aweme_count', 0),
                "data_source": "api"
            }
            
            logger.info(f"从API成功提取账号数据: {account_data['nickname']}")
            return account_data
    except Exception as e:
        logger.error(f"提取API账号数据时出错: {str(e)}")
    
    # 如果API数据提取失败，尝试从其他位置获取
    try:
        # 尝试获取页面注入的全局变量
        alternate_js = """
        () => {
            if (typeof window.__interceptedDouyinProfileData !== 'undefined') {
                return window.__interceptedDouyinProfileData;
            }
            return null;
        }
        """
        
        api_data = await page.evaluate(alternate_js)
        
        if api_data and 'data' in api_data:
            try:
                user_info = api_data['data'].get('user', {})
                
                # 处理用户数据
                account_data = {
                    "nickname": user_info.get('nickname', ''),
                    "signature": user_info.get('signature', ''),
                    "follower_count": user_info.get('follower_count', 0),
                    "following_count": user_info.get('following_count', 0),
                    "likes_received": user_info.get('total_favorited', 0),
                    "verified": user_info.get('custom_verify', '') != '',
                    "account_url": account_url,
                    "unique_id": user_info.get('unique_id', ''),
                    "sec_uid": user_info.get('sec_uid', sec_uid),
                    "account_type": user_info.get('account_type', 0),
                    "avatar_url": user_info.get('avatar_larger', {}).get('url_list', [''])[0],
                    "video_count": user_info.get('aweme_count', 0),
                    "data_source": "api"
                }
                
                logger.info(f"成功从全局变量中提取账号数据: {account_data['nickname']}")
                return account_data
            except Exception as e:
                logger.error(f"处理API账号数据时出错: {str(e)}")
    except Exception as e:
        logger.warning(f"提取备用API数据时出错: {str(e)}")
    
    # 最后尝试从DOM提取
    logger.info("尝试从DOM提取账号数据...")
    
    try:
        dom_data = await page.evaluate("""() => {
            if (typeof window.extractUserInfoFromDOM === 'function') {
                return window.extractUserInfoFromDOM();
            }
            
            // 如果函数不存在，尝试自己实现
            try {
                // 尝试从页面中提取用户信息
                let username = '';
                let following = 0;
                let followers = 0;
                let likes = 0;
                
                // 尝试多种可能的选择器
                // 用户名
                const possibleNameSelectors = ['h1', '.profile-name', '.account-name', '.user-name', 
                   '.author-card-user-name', '.account-name'];
                for (const selector of possibleNameSelectors) {
                    const el = document.querySelector(selector);
                    if (el && el.textContent.trim()) {
                        username = el.textContent.trim();
                        break;
                    }
                }
                
                // 尝试查找包含数字的元素
                const numberElements = Array.from(document.querySelectorAll('*')).filter(el => {
                    const text = el.textContent;
                    return text && 
                    (text.match(/\\d+(\\.\\d+)?[万亿k]?\\s*关注/) || 
                     text.match(/\\d+(\\.\\d+)?[万亿k]?\\s*粉丝/) ||
                     text.match(/\\d+(\\.\\d+)?[万亿k]?\\s*获赞/));
                });
                
                for (const el of numberElements) {
                    const text = el.textContent.trim();
                    if (text.match(/\\d+(\\.\\d+)?[万亿k]?\\s*关注/)) {
                        const num = text.match(/(\\d+(\\.\\d+)?)[万亿k]?/);
                        if (num) {
                            let value = parseFloat(num[1]);
                            if (text.includes('万')) value *= 10000;
                            if (text.includes('亿')) value *= 100000000;
                            following = value;
                        }
                    } else if (text.match(/\\d+(\\.\\d+)?[万亿k]?\\s*粉丝/)) {
                        const num = text.match(/(\\d+(\\.\\d+)?)[万亿k]?/);
                        if (num) {
                            let value = parseFloat(num[1]);
                            if (text.includes('万')) value *= 10000;
                            if (text.includes('亿')) value *= 100000000;
                            followers = value;
                        }
                    } else if (text.match(/\\d+(\\.\\d+)?[万亿k]?\\s*获赞/)) {
                        const num = text.match(/(\\d+(\\.\\d+)?)[万亿k]?/);
                        if (num) {
                            let value = parseFloat(num[1]);
                            if (text.includes('万')) value *= 10000;
                            if (text.includes('亿')) value *= 100000000;
                            likes = value;
                        }
                    }
                }
                
                return {
                    username,
                    following,
                    followers,
                    likes,
                    data_source: 'dom'
                };
            } catch (e) {
                console.error('从DOM提取用户信息时出错:', e);
                return { error: e.message, data_source: 'error' };
            }
        }""")
        
        if dom_data:
            # 构建账号数据
            account_data = {
                "nickname": dom_data.get('username', '未知用户'),
                "signature": "",
                "follower_count": dom_data.get('followers', 0),
                "following_count": dom_data.get('following', 0),
                "likes_received": dom_data.get('likes', 0),
                "verified": False,
                "account_url": account_url,
                "unique_id": "",
                "sec_uid": sec_uid,
                "account_type": 0,
                "avatar_url": "",
                "video_count": 0,
                "data_source": "dom"
            }
            
            logger.info(f"从DOM成功提取账号数据: {account_data['nickname']}")
            return account_data
    except Exception as e:
        logger.error(f"从DOM提取账号数据时出错: {str(e)}")
    
    # 如果所有方法都失败，返回基本信息
    logger.warning("无法提取详细账号数据，返回基本信息")
    return {
        "nickname": "未知用户",
        "signature": "",
        "follower_count": 0,
        "following_count": 0,
        "likes_received": 0,
        "verified": False,
        "account_url": account_url,
        "unique_id": "",
        "sec_uid": sec_uid,
        "account_type": 0,
        "avatar_url": "",
        "video_count": 0,
        "data_source": "fallback"
    }


async def extract_video_data(page: Page) -> List[Dict[str, Any]]:
    """
    从页面提取视频数据
    
    Args:
        page: Playwright 页面对象
        
    Returns:
        视频数据列表
    """
    logger.info("正在提取视频数据...")
    
    # 获取所有批次的API数据
    all_videos = []
    deduplication_set = set()  # 用于去重
    
    # 首先尝试从多批次API数据中提取
    api_js = """
    () => {
        const processVideoData = (data) => {
            const videos = [];
            if (data && data.data && data.data.aweme_list) {
                data.data.aweme_list.forEach(video => {
                    videos.push({
                        aweme_id: video.aweme_id,
                        title: video.desc || '',
                        create_time: video.create_time,
                        statistics: video.statistics || {},
                        video_info: {
                            duration: video.video && video.video.duration || 0,
                            cover: video.video && video.video.cover || {}
                        },
                        data_source: 'api'
                    });
                });
            }
            return videos;
        };
        
        const results = {
            all_data_sources: [],
            videos: []
        };
        
        // 处理多批次数据
        if (window.__interceptedDouyinDataList && window.__interceptedDouyinDataList.length > 0) {
            results.all_data_sources.push('batch_list');
            window.__interceptedDouyinDataList.forEach(data => {
                const videos = processVideoData(data);
                results.videos = results.videos.concat(videos);
            });
        }
        
        // 处理单次数据
        if (window.__interceptedDouyinData) {
            results.all_data_sources.push('single_data');
            const videos = processVideoData(window.__interceptedDouyinData);
            videos.forEach(video => {
                // 只添加不存在于前一批次的视频
                if (!results.videos.some(v => v.aweme_id === video.aweme_id)) {
                    results.videos.push(video);
                }
            });
        }
        
        // 去重处理
        const uniqueVideos = [];
        const processedIds = new Set();
        
        results.videos.forEach(video => {
            if (video.aweme_id && !processedIds.has(video.aweme_id)) {
                processedIds.add(video.aweme_id);
                uniqueVideos.push(video);
            }
        });
        
        results.videos = uniqueVideos;
        results.total_count = uniqueVideos.length;
        
        return results;
    }
    """
    
    try:
        api_results = await page.evaluate(api_js)
        
        if api_results and api_results.get('videos'):
            videos = api_results.get('videos', [])
            
            for video in videos:
                try:
                    # 检查是否已处理过此视频
                    if video.get('aweme_id') in deduplication_set:
                        continue
                    
                    deduplication_set.add(video.get('aweme_id'))
                    
                    # 提取视频详细信息
                    statistics = video.get('statistics', {})
                    video_data = {
                        "title": video.get('title', ''),
                        "video_url": f"https://www.douyin.com/video/{video.get('aweme_id', '')}",
                        "like_count": statistics.get('digg_count', 0),
                        "comment_count": statistics.get('comment_count', 0),
                        "share_count": statistics.get('share_count', 0),
                        "collect_count": statistics.get('collect_count', 0),
                        "play_count": statistics.get('play_count', 0),
                        "aweme_id": video.get('aweme_id', ''),
                        "create_time": video.get('create_time', 0),
                        "duration": video.get('video_info', {}).get('duration', 0),
                        "cover_url": video.get('video_info', {}).get('cover', {}).get('url_list', [''])[0] if 
                                   video.get('video_info', {}).get('cover', {}).get('url_list') else '',
                        "data_source": "api"
                    }
                    all_videos.append(video_data)
                except Exception as e:
                    logger.error(f"处理单个视频数据时出错: {str(e)}")
            
            logger.info(f"从API成功提取 {len(all_videos)} 个视频")
            
            # 如果成功提取了视频，直接返回
            if all_videos:
                # 按创建时间排序
                all_videos.sort(key=lambda x: x.get('create_time', 0), reverse=True)
                return all_videos
    except Exception as e:
        logger.error(f"处理API视频数据时出错: {str(e)}")
    
    # 如果API数据提取失败或没有视频，尝试从其他方式提取
    try:
        # 从注入脚本的全局变量中提取
        intercepted_data_list = await page.evaluate("""() => {
            if (window.__interceptedDouyinDataList && window.__interceptedDouyinDataList.length > 0) {
                return window.__interceptedDouyinDataList;
            } else if (window.__interceptedDouyinData) {
                return [window.__interceptedDouyinData];
            }
            return [];
        }""")
        
        if intercepted_data_list:
            for batch in intercepted_data_list:
                try:
                    # 提取视频列表
                    videos = batch.get('data', {}).get('aweme_list', [])
                    
                    for video in videos:
                        try:
                            # 检查是否已处理过此视频
                            if video.get('aweme_id') in deduplication_set:
                                continue
                                
                            deduplication_set.add(video.get('aweme_id'))
                            
                            # 提取视频详细信息
                            video_data = {
                                "title": video.get('desc', ''),
                                "video_url": f"https://www.douyin.com/video/{video.get('aweme_id', '')}",
                                "like_count": video.get('statistics', {}).get('digg_count', 0),
                                "comment_count": video.get('statistics', {}).get('comment_count', 0),
                                "share_count": video.get('statistics', {}).get('share_count', 0),
                                "collect_count": video.get('statistics', {}).get('collect_count', 0),
                                "play_count": video.get('statistics', {}).get('play_count', 0),
                                "aweme_id": video.get('aweme_id', ''),
                                "create_time": video.get('create_time', 0),
                                "duration": video.get('video', {}).get('duration', 0),
                                "cover_url": video.get('video', {}).get('cover', {}).get('url_list', [''])[0] if 
                                           video.get('video', {}).get('cover', {}).get('url_list') else '',
                                "data_source": "api"
                            }
                            all_videos.append(video_data)
                        except Exception as e:
                            logger.error(f"处理单个视频数据时出错: {str(e)}")
                except Exception as e:
                    logger.error(f"处理批次视频数据时出错: {str(e)}")
                    
            if all_videos:
                logger.info(f"从全局变量成功提取 {len(all_videos)} 个视频")
                
                # 按创建时间排序
                all_videos.sort(key=lambda x: x.get('create_time', 0), reverse=True)
                return all_videos
    except Exception as e:
        logger.error(f"从全局变量提取视频数据时出错: {str(e)}")
    
    # 如果上述方法都失败，尝试从DOM提取
    logger.info("尝试从DOM提取视频数据...")
    
    try:
        dom_videos = await page.evaluate("""() => {
            const videos = document.querySelectorAll('.xg-video-container');
            return Array.from(videos).map(video => {
                // 尝试提取各种数据
                const titleEl = video.querySelector('.title');
                const title = titleEl ? titleEl.textContent.trim() : '';
                
                // 尝试提取链接
                const linkEl = video.querySelector('a');
                const link = linkEl ? linkEl.href : '';
                
                // 尝试提取封面图
                const imgEl = video.querySelector('img');
                const coverUrl = imgEl ? imgEl.src : '';
                
                // 尝试提取数字
                const stats = {};
                const statElements = video.querySelectorAll('.count-item');
                statElements.forEach(statEl => {
                    const text = statEl.textContent.trim();
                    if (text.includes('赞')) {
                        stats.likes = text.replace(/[^0-9.万亿k]/g, '');
                    } else if (text.includes('评论')) {
                        stats.comments = text.replace(/[^0-9.万亿k]/g, '');
                    } else if (text.includes('收藏')) {
                        stats.collects = text.replace(/[^0-9.万亿k]/g, '');
                    } else if (text.includes('播放量') || text.includes('观看')) {
                        stats.plays = text.replace(/[^0-9.万亿k]/g, '');
                    }
                });
                
                // 从链接中提取aweme_id
                let aweme_id = '';
                try {
                    if (link) {
                        const match = link.match(/\\/video\\/([^/?]+)/);
                        if (match && match[1]) {
                            aweme_id = match[1];
                        }
                    }
                } catch (e) {
                    console.error('提取视频ID时出错:', e);
                }
                
                return {
                    title,
                    link,
                    coverUrl,
                    aweme_id,
                    ...stats
                };
            });
        }""")
        
        if dom_videos:
            for i, video in enumerate(dom_videos):
                try:
                    # 检查是否已经处理过此视频
                    aweme_id = video.get('aweme_id', f"dom_{i}")
                    if aweme_id in deduplication_set:
                        continue
                        
                    deduplication_set.add(aweme_id)
                    
                    # 解析数字
                    like_count = parse_count(video.get('likes', '0'))
                    comment_count = parse_count(video.get('comments', '0'))
                    collect_count = parse_count(video.get('collects', '0'))
                    play_count = parse_count(video.get('plays', '0'))
                    
                    # 构建视频数据
                    video_data = {
                        "title": video.get('title', ''),
                        "video_url": video.get('link', ''),
                        "like_count": like_count,
                        "comment_count": comment_count,
                        "share_count": 0,
                        "collect_count": collect_count,
                        "play_count": play_count,
                        "aweme_id": aweme_id,
                        "create_time": int(time.time()),
                        "duration": 0,
                        "cover_url": video.get('coverUrl', ''),
                        "data_source": "dom"
                    }
                    all_videos.append(video_data)
                except Exception as e:
                    logger.error(f"处理DOM视频数据时出错: {str(e)}")
            
            logger.info(f"从DOM成功提取 {len(dom_videos)} 个视频")
    except Exception as e:
        logger.error(f"从DOM提取视频数据时出错: {str(e)}")
    
    # 按创建时间排序
    all_videos.sort(key=lambda x: x.get('create_time', 0), reverse=True)
    
    return all_videos


def parse_count(text: str) -> int:
    """
    解析数字文本（处理"万"、"亿"等单位）
    
    Args:
        text: 数字文本
        
    Returns:
        整数值
    """
    try:
        if not text or text == "":
            return 0
            
        text = text.strip().replace(',', '')
        
        if '万' in text:
            num = float(text.replace('万', ''))
            return int(num * 10000)
        elif '亿' in text:
            num = float(text.replace('亿', ''))
            return int(num * 100000000)
        elif 'w' in text.lower() or 'W' in text:
            num = float(text.lower().replace('w', ''))
            return int(num * 10000)
        elif 'k' in text.lower() or 'K' in text:
            num = float(text.lower().replace('k', ''))
            return int(num * 1000)
        else:
            return int(float(text))
    except:
        return 0 