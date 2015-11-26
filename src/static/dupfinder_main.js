var sch_mode = 'stdmode';   // rb can change to 'cmpmode'

$(function () {    
    var pstyle = 'border: 1px solid #dfdfdf; padding: 5px;';

    $('#toolbar').w2toolbar({
        name: 'toolbar',
        items: [
            { type: 'html', id: 'label_html', html: '<h3>Duplicate File Finder</h3>' },
            { type: 'spacer' }, 
            { type: 'radio', id: 'duplicates_r', group: '1', caption: 'Find Duplicates', icon: 'fa-star', checked: true}, 
            { type: 'radio', id: 'compare_r', group: '1', caption: 'Compare Two Folders', icon: 'fa-star' }
        ]
        //[refcode]
        //onClick: function(event) { 
        //    console.log('EVENT: '+ event.type + ' TARGET: '+ event.target, event);
        //}

    });




    // html for buttons on left panel
    left_panel_buttons = '<button id="sch_folders" class="btn" style="width:90%">Search Folder(s)</button>' +
                         '<button id="sch" class="btn" style="width:90%">Search</button>' +
                         '<button id="clr_folders" class="btn" style="width:90%">Clear Folders</button>' +
                         '<button id="clr_console" class="btn" style="width:90%">Clear Console</button>' +
                         '<div><h4> Extra Options </h4>'


    $('#layout').w2layout({
        name: 'layout',
        panels: [
            { type: 'left', size: 150, resizable: false, style: pstyle, content: left_panel_buttons },   // 'left'
            { type: 'main', style: pstyle, content: 'main', // , title: 'main' },
                toolbar:  { 
                    items: [ 
                        {type: 'button', id: 'plus_b', caption: 'Add Search Folder', icon: 'w2ui-icon-plus'},
                        {type: 'html', id: 'sch_input_html', html: '<input size="80%"/>'}  // get size of panel
                    ]
                },
            },
            { type: 'bottom', size: '60%', style: pstyle, // , title: 'bottom', 
                tabs: [ 
                    {id: 'main_tab',     caption: 'Main'},
                    {id: 'stdview_tab',  caption: 'Standard View'},
                    {id: 'compview_tab', caption: 'Compare View'}
                    ]
            }
        ]
    });
   
    // default tab selection
    w2ui.layout.panels[2].tabs.active = 'main_tab'; 
    w2ui.layout.panels[2].tabs.refresh();

    // get toolbar state
    w2ui.toolbar.on('click', function (event) { // replace 'click' w/* for any event (and get event.type)
        sch_mode = (event.target==='compare_r') ? 'cmpmode' : 'stdmode';   
        w2ui.toolbar.refresh();

        console.log('check status of std' + w2ui.toolbar.items[2].checked)
        console.log('check status of cmp' + w2ui.toolbar.items[3].checked)
    });

    // specify content for main panel 
    w2ui.layout.content('main', $().w2grid({
            name: 'folders_sch_grid', 
            columns: [ {field: 'folder', caption: 'Folder', size: '100%'} ],
            records: []
        })
    );


    // -- event handlers(for buttons) AJAX calls --

    // TODO. sch_mode must be encoded as toolbar state in json not as route ?
    $("#sch_folders").click(function() {
        // alert("You clicked something");

        console.log('sch_mode is ' + sch_mode); 
        $.get('search/' + sch_mode, {fname: 'mahmud', lname: 'hassan'}, function(response) {
            received = response.search_results;
            alert(received);
        });
    });

    $("#sch").click(function() {
        // alert("You clicked something");
        $.get('searchmode/std', {}, function(response) {
            alert(response);
        });
    });

});

