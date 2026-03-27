(function () {
    const runtimeConfig = window.APP_CONFIG || {};

    const serviceUrls = {
        user: runtimeConfig.USER_SERVICE_URL,
        booking: runtimeConfig.BOOKING_SERVICE_URL,
        notification: runtimeConfig.NOTIFICATION_SERVICE_URL,
        event: runtimeConfig.EVENT_SERVICE_URL,
        payment: runtimeConfig.PAYMENT_SERVICE_URL
    };

    function joinUrl(base, path) {
        const normalizedBase = String(base || "").replace(/\/$/, "");
        const normalizedPath = String(path || "").startsWith("/") ? path : `/${path}`;
        return `${normalizedBase}${normalizedPath}`;
    }

    window.buildApiUrl = function (service, path) {
        if (!serviceUrls[service]) {
            throw new Error(`Unknown service key: ${service}`);
        }
        return joinUrl(serviceUrls[service], path);
    };
})();
