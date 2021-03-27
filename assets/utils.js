window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        get_window_width: function() {
            return window.innerWidth;
        },

        get_window_height: function() {
            return window.innerHeight;
        }
    }
});