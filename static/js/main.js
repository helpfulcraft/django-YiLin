// DOM加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 自动关闭提示消息
    initAlerts();
    // 初始化工具提示
    initTooltips();
    // 初始化返回顶部按钮
    initBackToTop();
    // 初始化图片预览
    initImagePreview();
});

// 初始化提示消息
function initAlerts() {
    var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// 初始化工具提示
function initTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// 初始化返回顶部按钮
function initBackToTop() {
    // 创建返回顶部按钮
    var backToTop = document.createElement('button');
    backToTop.id = 'back-to-top';
    backToTop.className = 'btn btn-primary position-fixed bottom-0 end-0 m-3 rounded-circle';
    backToTop.style.display = 'none';
    backToTop.innerHTML = '<i class="bi bi-arrow-up"></i>';
    document.body.appendChild(backToTop);

    // 监听滚动事件
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTop.style.display = 'block';
        } else {
            backToTop.style.display = 'none';
        }
    });

    // 点击返回顶部
    backToTop.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// 初始化图片预览
function initImagePreview() {
    var images = document.querySelectorAll('.news-content img, .activity-content img');
    images.forEach(function(img) {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            var modal = new bootstrap.Modal(document.getElementById('imagePreviewModal') || createImagePreviewModal());
            document.querySelector('#imagePreviewModal .modal-body img').src = this.src;
            modal.show();
        });
    });
}

// 创建图片预览模态框
function createImagePreviewModal() {
    var modalHtml = `
        <div class="modal fade" id="imagePreviewModal" tabindex="-1">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-body p-0">
                        <img src="" class="img-fluid" alt="预览图片">
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    return document.getElementById('imagePreviewModal');
}

// 表单验证
function validateForm(formId) {
    var form = document.getElementById(formId);
    if (!form) return false;

    var isValid = true;
    var inputs = form.querySelectorAll('input[required], textarea[required], select[required]');

    inputs.forEach(function(input) {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
