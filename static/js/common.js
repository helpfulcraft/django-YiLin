// 网络请求监控
(function() {
    // 监控 XMLHttpRequest
    let originalXHR = window.XMLHttpRequest;
    function newXHR() {
        let xhr = new originalXHR();
        
        // 监听请求
        xhr.addEventListener('load', function() {
            console.log('XHR 请求完成:', {
                url: xhr._url,
                method: xhr._method,
                status: xhr.status,
                response: xhr.response
            });
        });
        
        xhr.addEventListener('error', function() {
            console.error('XHR 请求失败:', {
                url: xhr._url,
                method: xhr._method,
                status: xhr.status
            });
        });
        
        // 重写 open 方法以捕获 URL 和方法
        let originalOpen = xhr.open;
        xhr.open = function(method, url) {
            xhr._url = url;
            xhr._method = method;
            return originalOpen.apply(this, arguments);
        };
        
        return xhr;
    }
    window.XMLHttpRequest = newXHR;
    
    // 监控 Fetch
    let originalFetch = window.fetch;
    window.fetch = function() {
        return originalFetch.apply(this, arguments)
            .then(response => {
                console.log('Fetch 请求完成:', {
                    url: arguments[0],
                    method: arguments[1]?.method || 'GET',
                    status: response.status
                });
                return response;
            })
            .catch(error => {
                console.error('Fetch 请求失败:', {
                    url: arguments[0],
                    method: arguments[1]?.method || 'GET',
                    error: error
                });
                throw error;
            });
    };
})();

// 性能监控
(function() {
    if (window.performance && window.performance.timing) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                let timing = window.performance.timing;
                let performanceInfo = {
                    // DNS 查询时间
                    dns: timing.domainLookupEnd - timing.domainLookupStart,
                    // TCP 连接时间
                    tcp: timing.connectEnd - timing.connectStart,
                    // 首字节时间
                    ttfb: timing.responseStart - timing.navigationStart,
                    // DOM 解析时间
                    domParse: timing.domComplete - timing.domInteractive,
                    // 页面完全加载时间
                    loadComplete: timing.loadEventEnd - timing.navigationStart
                };
                console.log('页面性能数据:', performanceInfo);
            }, 0);
        });
    }
})();

// 资源加载监控
(function() {
    window.addEventListener('error', function(e) {
        if (e.target.tagName) {
            console.error('资源加载失败:', {
                type: e.target.tagName.toLowerCase(),
                url: e.target.src || e.target.href,
                error: e.error
            });
        }
    }, true);
})();
