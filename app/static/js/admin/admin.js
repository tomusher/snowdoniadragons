$(document).ready(function() {
    function boardgameSelectize(target) {
        $(target).parents('.object').css('overflow', 'visible');
        $(target).parents('.multiple').css('overflow', 'visible');
        $(target).css('overflow', 'visible');
        $('.boardgame-selectize select', target).selectize({
            mode: 'single',
            valueField: 'id',
            labelField: 'name',
            searchField: 'name',
            load: function(query, callback) {
                if(!query.length) return callback();
                $.ajax({
                    url: '/search-games/?query='+encodeURIComponent(query),
                    type: 'GET',
                    error: function() {
                        callback()
                    },
                    success: function(res) {
                        callback(res.results)
                    },
                })
            }
        })
    }
    boardgameSelectize($('#id_games_played-FORMS'));
    $('body').on('DOMNodeInserted', '#id_games_played-FORMS', function(event) {
        if($(event.target).parent('#id_games_played-FORMS')) {
            boardgameSelectize(event.target);
        }
    })
    initDateSlugAutoPopulate();
});


function initDateSlugAutoPopulate() {
    $('#id_date').on('keyup keydown keypress blur', function() {
        var slugifiedTitle = cleanDateForSlug(this.value);
        $('#id_slug').val(slugifiedTitle);
    });
}

function cleanDateForSlug(val, useURLify) {
    var date = new Date(val);
    var month = ('0' + (date.getMonth()+1)).slice(-2);
    var dateString = date.getFullYear() + "-" + month + "-" + date.getDate();
    return URLify(dateString);
}
