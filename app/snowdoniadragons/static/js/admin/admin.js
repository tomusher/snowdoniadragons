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
});
