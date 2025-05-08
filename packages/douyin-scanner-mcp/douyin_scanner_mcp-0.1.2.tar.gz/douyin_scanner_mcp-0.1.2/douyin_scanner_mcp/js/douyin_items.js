(function() {
  // 保存原始的 XMLHttpRequest 方法
  const originalOpen = XMLHttpRequest.prototype.open;
  const originalSend = XMLHttpRequest.prototype.send;
  const originalSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;

  // 设置上下文存活标志
  window.__contextAlive = true;
  
  // 创建一个数组用于存储多个API响应
  window.__interceptedDouyinDataList = [];

  // Hook open 方法
  XMLHttpRequest.prototype.open = function() {
    // 保存 open 参数供 send 方法使用
    this.openArgs = arguments;
    return originalOpen.apply(this, arguments);
  };

  // Hook send 方法 
  XMLHttpRequest.prototype.send = function() {
    const xhr = this;
    const openArgs = this.openArgs;
    const sendArgs = arguments;

    // 添加响应拦截
    xhr.addEventListener('load', function() {
      try {
        // 只针对抖音特定 URL 进行处理
        if (openArgs[1].includes('/aweme/v1/web/aweme/post/') || 
            openArgs[1].includes('/aweme/v1/web/user/profile/other/')) {
          try {
            // 解析 JSON 响应
            const data = JSON.parse(xhr.responseText);
            
            if (openArgs[1].includes('/aweme/v1/web/aweme/post/')){
              // 检查URL中是否包含游标参数，用于判断是否为分页请求
              const isPagedRequest = openArgs[1].includes('cursor=') || openArgs[1].includes('max_cursor=');
              
              // 保存到全局变量
              window.__interceptedDouyinData = {
                url: openArgs[1],
                status: xhr.status,
                data: data,
                timestamp: Date.now(),
                info: {
                  'name': "douyinPostData",
                  'isPaged': isPagedRequest
                }
              };
              
              // 将每个响应都添加到列表中，用于合并处理
              const shouldAddToList = data?.data?.aweme_list?.length > 0;
              if (shouldAddToList) {
                window.__interceptedDouyinDataList.push({
                  url: openArgs[1],
                  status: xhr.status,
                  data: data,
                  timestamp: Date.now(),
                  info: {
                    'name': "douyinPostData",
                    'isPaged': isPagedRequest
                  }
                });
                console.log(`已拦截并保存抖音视频数据，当前共有 ${window.__interceptedDouyinDataList.length} 个批次，本批次有 ${data?.data?.aweme_list?.length || 0} 个视频`);
              }
              
              console.log('拦截到抖音视频数据');
            }

            if (openArgs[1].includes('/aweme/v1/web/user/profile/other/')){
              // 保存到全局变量
              window.__interceptedDouyinProfileData = {
                url: openArgs[1],
                status: xhr.status,
                data: data,
                timestamp: Date.now(),
                info: {
                  'name': "douyinProfileData"
                }
              };
              
              console.log('拦截到抖音个人资料数据');
            }

            // 记录日志
            const logEntry = {
              type: 'Douyin_INTERCEPT',
              timestamp: Date.now(),
              request: {
                method: openArgs[0] || 'GET',
                url: openArgs[1]
              },
              response: {
                status: xhr.status,
                data_source: 'api'
              }
            };

            console.log('Douyin_INTERCEPT:' + JSON.stringify(logEntry));
          } catch(err) {
            // 如果JSON解析失败,记录文本内容
            console.error('解析JSON失败:', err);
          }
        }
      } catch (e) {
        console.error('拦截处理时出错:', e);
      }
    });

    // 调用原始 send 方法
    return originalSend.apply(this, sendArgs);
  };
  
  // 添加全局辅助函数，用于检查是否已捕获数据
  window.checkInterceptedData = function() {
    return {
      hasProfileData: typeof window.__interceptedDouyinProfileData !== 'undefined',
      hasVideoData: typeof window.__interceptedDouyinData !== 'undefined',
      hasMultipleData: typeof window.__interceptedDouyinDataList !== 'undefined' && window.__interceptedDouyinDataList.length > 0,
      dataCount: typeof window.__interceptedDouyinDataList !== 'undefined' ? window.__interceptedDouyinDataList.length : 0
    };
  };
  
  // 额外的辅助函数，用于主动探测用户数据
  window.extractUserInfoFromDOM = function() {
    try {
      // 尝试从页面中提取用户信息
      let username = '';
      let following = 0;
      let followers = 0;
      let likes = 0;
      
      // 尝试多种可能的选择器
      // 用户名
      const possibleNameSelectors = ['h1', '.profile-name', '.account-name', '.user-name'];
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
          (text.match(/\d+(\.\d+)?[万亿k]?\s*关注/) || 
           text.match(/\d+(\.\d+)?[万亿k]?\s*粉丝/) ||
           text.match(/\d+(\.\d+)?[万亿k]?\s*获赞/));
      });
      
      for (const el of numberElements) {
        const text = el.textContent.trim();
        if (text.match(/\d+(\.\d+)?[万亿k]?\s*关注/)) {
          const num = text.match(/(\d+(\.\d+)?)[万亿k]?/);
          if (num) {
            let value = parseFloat(num[1]);
            if (text.includes('万')) value *= 10000;
            if (text.includes('亿')) value *= 100000000;
            following = value;
          }
        } else if (text.match(/\d+(\.\d+)?[万亿k]?\s*粉丝/)) {
          const num = text.match(/(\d+(\.\d+)?)[万亿k]?/);
          if (num) {
            let value = parseFloat(num[1]);
            if (text.includes('万')) value *= 10000;
            if (text.includes('亿')) value *= 100000000;
            followers = value;
          }
        } else if (text.match(/\d+(\.\d+)?[万亿k]?\s*获赞/)) {
          const num = text.match(/(\d+(\.\d+)?)[万亿k]?/);
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
  };
  
  console.log('抖音数据拦截脚本已注入');
})(); 