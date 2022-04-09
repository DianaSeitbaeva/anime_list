var HomeworksListPage = {
    init: function() {
        this.$container = $('.homeworks-container');
        this.render();
        this.bindEvents();
    },
    render: function() {},
    bindEvents: function() {
        $('.btn-checked', this.$container).on('click', function(e) {
            e.preventDefault();
            var self = $(this);
            var url = $(this).attr('href');
            $.getJSON(url, function(result) {
                if (result.success) {
                    $('.glyphicon-ok', self).toggleClass('active');
                }
            });
            return false;
        });
    }
};
var FilesListPage = {
    init: function() {
        this.$container = $('.files-container');
        this.render();
        this.bindEvents();
    },
    render: function() {},
    bindEvents: function() {
        $('.btn-checked', this.$container).on('click', function(e) {
            e.preventDefault();
            var self = $(this);
            var url = $(this).attr('href');
            $.getJSON(url, function(result) {
                if (result.success) {
                    $('.glyphicon-ok', self).toggleClass('active');
                }
            });
            return false;
        });
    }
};
$(document).ready(function() {
    HomeworksListPage.init();
    FilesListPage.init();
});
