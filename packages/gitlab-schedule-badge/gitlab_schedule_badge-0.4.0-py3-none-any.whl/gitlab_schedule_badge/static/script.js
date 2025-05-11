/* adjust fetch button based on sane url value */
$('#query-url').on('input',function(e) {
    $('#query-submit').attr("disabled", true);

    var rawUrl = $(this).val().split('/-/')[0].trim();
    if (rawUrl.indexOf(' ') >= 0) return;

    try {
        const parsedUrl = new URL(rawUrl);
        var urlParts = parsedUrl.pathname.split('/')
        if (urlParts.length > 2) {
            for (let i = 1; i < urlParts.length; i++) {
                if (!urlParts[i]) return;
            }

            $('#query-submit').attr("disabled", false);
        }
    } catch (err) {}
});

function buildExample(data) {
    const imgurl_block = document.createElement("div");
    imgurl_block.setAttribute('class', 'container');

    const imgurl_input = document.createElement("textarea");
    imgurl_input.setAttribute('aria-readonly', 'true');
    imgurl_input.setAttribute('class', 'badge-url');
    imgurl_input.setAttribute('readonly', 'readonly');
    imgurl_input.setAttribute('spellcheck', 'false');
    imgurl_input.textContent = data
    imgurl_block.append(imgurl_input);

    $('#pipeline-schedules').append(imgurl_block);
}

$('form').submit(function (e) {
    query_url = $('#query-url').val().split('/-/')[0].trim()

    e.preventDefault();
    $('#query-submit').attr("disabled", true);
    $('#url-examples').remove();
    const data = {
        url: query_url,
    };

    $('#pipeline-schedules').empty();
    $('#project-name').text("Querying...");
    $('#project-name').unwrap('a');
    $('#results').css('display', 'block');

    $.ajax({
        type: 'POST',
        url: 'find',
        data: JSON.stringify(data),
        contentType: 'application/json',
    })
    .done((data) => {
        admin_cfg_url = query_url + '/-/pipeline_schedules'

        $('#project-name').text(data['project']);
        $('#project-name').wrap(
            '<a href="' + admin_cfg_url + '" target="_blank"></a>');
        for (const entry of data['schedules']) {
            desc = encodeURIComponent(entry['description'])
            imgurl = entry['badge_url']

            const badge_block = document.createElement("div")

            let container = badge_block
            if (entry['url']) {
                const badge_ahref = document.createElement("a")
                badge_ahref.setAttribute('href', entry['url']);
                badge_ahref.setAttribute('target', '_blank');
                badge_block.append(badge_ahref);

                container = badge_ahref
            }

            const badge_img = document.createElement("img")
            badge_img.setAttribute('src', imgurl);
            container.append(badge_img);
            $('#pipeline-schedules').append(badge_block);

            // raw example
            buildExample(imgurl);
            // Custom label
            buildExample(imgurl + '/Custom%20Name');
            // HTML helper
            buildExample(`\
<a href="` + query_url + `">
    <img src="` + imgurl + `" />
</a>`);
            // Markdown helper
            buildExample(`\
[![](` + imgurl + `)](` + query_url + `)`);
            // reStructuredText helper
            buildExample(`\
.. image:: ` + imgurl + `
   :target: ` + query_url);
        }

        if (data['schedules'].length == 0) {
            $('#pipeline-schedules').append(
                '<div>Project has no scheduled pipelines.</div>'
            );
        }
    })
    .fail((err) => {
        $('#project-name').text("Query Failure");
        $('#project-name').unwrap('a');
        if (err.responseJSON) {
            rsp = '<div>' + err.responseJSON['message'] + '</div>'
        } else {
            rsp = '<div>Unknown failure. Try refreshing page?</div>'
        }
        $('#pipeline-schedules').append(rsp);
    })
    .always(() => {
        setTimeout(function() {
            $('#query-submit').attr("disabled", false);
        }, 1000);
    });
});

$('body').on('click', '.badge-url', function() {
    $(this).select();
});
