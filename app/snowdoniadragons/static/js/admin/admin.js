$(document).ready(function() {
    function boardgameSelectize() {
        $('.boardgame-selectize select').selectize({
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
                    }
                })
            }
        })
    }
    boardgameSelectize()
    $('body').on('DOMNodeInserted', 'li', function() {
        boardgameSelectize()
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
