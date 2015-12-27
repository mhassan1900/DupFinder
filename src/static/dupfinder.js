
$(function () {    
    var pstyle = 'border: 1px solid #dfdfdf; padding: 5px;';
    var search_mode = 'stdmode';   // rb can change to 'cmpmode'

    // var window_height = $(window).innerHeight();    

    // -- TITLE TOOLBAR ON TOP OF MAIN LAYOUT --

    $('#title_toolbar').w2toolbar({
        name: 'toolbar',
        items: [
            { type: 'html', html: '<h2>Duplicate File Finder</h2>' },
            { type: 'spacer' }, 
            { type: 'radio', id: 'duplicates_r', group: '1', caption: 'Find Duplicates', icon: 'fa-star', checked: true}, 
            { type: 'radio', id: 'compare_r', group: '1', caption: 'Compare Two Folders', icon: 'fa-star' }
        ]
        //[refcode]
        //onClick: function(event) { 
        //    console.log('EVENT: '+ event.type + ' TARGET: '+ event.target, event);
        //}

    });



    // -- BODY LAYOUT FOR MAIN AREA left/main/bottom -- 

    // html for buttons on left panel
    var left_panel_buttons =  
        '<button id="select_folders" class="btn" style="width:90%;">Select Folders</button>' +
        '<button id="search" class="btn" style="width:90%;">Search</button>' +
        '<button id="clear_folders" class="btn" onclick="openPopup()" style="width:90%;">Clear Folders</button>' +
        '<button id="clear_console" class="btn" style="width:90%;">Clear Console</button>' +
        '<div><h5> Extra Options </h5>' + 
        '<button id="select_exclusions" class="btn" style="width:90%;">Select Exclusions</button>' +
        '<button id="skip_matches" class="btn" style="width:90%;">Skip Matches</button>'; 
    

    $('#body_layout').w2layout({
        name: 'layout',
        panels: [
            { type: 'left', size: 170, resizable: false, style: pstyle, content: left_panel_buttons },   
            { type: 'main', style: pstyle, content: 'main', // , title: 'main' },
                toolbar:  { 
                    name: 'main_toolbar',
                    items: [ 
                        {type: 'button', id: 'plus_add_folder', caption: 'Add Search Folder', icon: 'w2ui-icon-plus'},
                        {type: 'html', html: '<input id="search_folder_input" size="100%"/>'}  
                    ]
                },
            },
            { type: 'bottom', size: "60%", resizable: true, style: pstyle, 
              tabs: {
                active: 'main_tab',
                tabs: [ 
                    {id: 'main_tab',     caption: 'Main'},
                    {id: 'stdview_tab',  caption: 'Standard View'},
                    {id: 'cmpview_tab', caption: 'Compare View'},
                ],
                onClick: tabClick 
              },
            }
        ]
    });
 



    // get toolbar state
    w2ui.toolbar.on('click', function (event) { // replace 'click' w/* for any event (and get event.type)
        search_mode = (event.target==='compare_r') ? 'cmpmode' : 'stdmode';   
        w2ui.toolbar.refresh();
        // console.log('check status of std' + w2ui.toolbar.items[2].checked)
        // console.log('check status of cmp' + w2ui.toolbar.items[3].checked)
    });


    var folders2search = [];

    // specify content for main panel 
    w2ui.layout.content('main', $().w2grid({
            name: 'folders_sch_grid', 
            columns: [ {field: 'folder', caption: 'Folder', size: '100%'} ],
            records: []
        })
    );


    console.log("W2UI OBJECCT");
    console.log(w2ui);

    w2ui.layout_main_toolbar.on('click', function (event) {
        if (event.target === 'plus_add_folder') {
            var newfolder = $("#search_folder_input").val();
            idx = folders2search.indexOf(newfolder);
            if (idx > -1) {
                return;  
            }
            folders2search.push(newfolder);
            w2ui.folders_sch_grid.add({
                'recid': folders2search.length,
                'folder': newfolder
            });
        }
    });


    // -- event handlers(for buttons) AJAX calls --

    // TODO. search_mode must be encoded as toolbar state in json not as route ?
    $("#select_folders").click(function() {
        /* 
        // DEBUG 
        console.log('select folders are: ' + search_mode); 
        $.get('search/' + search_mode, {fname: 'mahmud', lname: 'hassan'}, function(response) {
            received = response.search_results;
            alert('sel folders: ' + received);
        });
        */
        console.log ("Value => " + $("#search_folder_input").val());
    });



    // OK 'getting' data & responses 
    var response_object = null; 

    $("#search").click(function() {
        $.ajax({
            url: 'search/' + search_mode, 
            contentType: "application/json",
            data: {'folders2search': JSON.stringify(folders2search)},
            success: function(response) {
                // set the tab & display data
                response_object = response['search_results'];
                tab_func = (search_mode === 'stdmode') ? display_stdview : display_cmpview;
                tab_func(response_object); 
            },
            error: function() {
                console.log ("ERROR. Did not get back search results correctly");
            }
        });

    });


    // -- Tab Click for Bottom Panel  & Related functions --

    var logview_data = []; 
    var stdview_data = {}; 
    var cmpview_data = {};

    function tabClick(event) {
        // event.target is [main_tab|cmpview_tab|stdview_tab]
        if (event.target === 'stdview_data') display_stdview(response_object);
        else if (event.target === 'cmpview_data') display_cmpiew(cmpview_data);
        else display_logview(logview_data);
    }

    
    function display_stdview(data) {
        w2ui.layout.panels[2].tabs.active = 'stdview_tab'; 
        w2ui.layout.panels[2].tabs.refresh();
        var response_content = ''; 
        console.log("response object");
        console.log(data); 
        if ((search_mode === 'stdmode') && (data)) { 
            for (var k in response_object) {
                response_content += '<h3>' + k + ':</h3><ul>';
                for (var r=0; r < response_object[k].length; r++) {
                    response_content +=  "<li> " + response_object[k][r] + "</li>";
                }
                response_content +=  "</ul>";
            }
        } else {
            response_content = 'Nothing to show!';
        }
        w2ui['layout'].content('bottom', response_content); 
    }


    function display_cmpview(data) {
        w2ui.layout.panels[2].tabs.active = 'cmpview_tab';
        w2ui.layout.panels[2].tabs.refresh();

        var response_content = ''; 
        console.log("response object");
        console.log(data); 
        if ((search_mode === 'cmpmode') && (data)) { 
            console.log ("GOT TO CMP MODE");
            for (var k in response_object) {
                response_content += '<h3>' + k + ':</h3><ul>';
                for (var r=0; r < response_object[k].length; r++) {
                    response_content +=  "<li> " + response_object[k][r] + "</li>";
                }
                response_content +=  "</ul>";
            }
        } else {
            response_content = 'Nothing to show!';
        }
        w2ui['layout'].content('bottom', response_content); 
    }

    function display_logview(data) {
        w2ui.layout.panels[2].tabs.active = 'mainview_tab';
        w2ui.layout.panels[2].tabs.refresh();
        if (!data)  
            return;
    }





/*

    // In case of a window resize
    $(window).resize(function () {
        window_height = $(window).innerHeight();
        // window_width = $(window).innerWidth();
        console.log('h & w are ' + window_height); 
        w2ui.layout.panels[2].refresh();
    });
*/


});
