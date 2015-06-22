/**** 
* multipart message generation based on translated templates
****/

var mep, editor; 
var txt_changed = false;
var language = 'en';
var small_group = false;  // set this to true if initial country selection is rendered useless by the small amount of meps (shadow+rapporteur)
var disabled = false;

$(function () {

  // insert html inputs via templates
  $(get_tmpl("message_inputs")).Chevron("render", {}, reference_message_inputs); 
  $(get_tmpl("mep_selection")).Chevron("render", {}, reference_mep_selection);

  if (disabled) {
    $('#sendfax').hide();
    $('#sent-message').show();
  }
  
});

// send fax
function sendfax() {
  var msg;
  $('#full_message').val(msg = (nicEditors.findEditor('full_message').getContent()||''));
  $('#id').val($('#id').val() || (mep||{}).id || '124935'); // sorry michel ;)
  if (msg != '' && msg.length > 140 && msg.length < 70000) {
    document.getElementById("faxform").submit();
  }
}

/**
* switch language 
**/
function setLng(l) {
  // add new languages here but make sure we have the templates files and they are embedded in fax-personal.tmpl
  if (['en', 'de', 'ro', 'fr', 'pl', 'nl'].indexOf(l) !== -1) {
    language = l;
  }
}

function update_language () {
  setLng($('#language_selector').val());
  $(get_tmpl("message_inputs")).Chevron("render", {}, function (result) {
    removeEditor();
    reference_message_inputs(result);
    load_user_input();
    $('#id').val((mep||{}).id || '124935'); // sorry michel ;)
  });
}

/***
* loading and displaying html elements and bind actions to them
***/
function reference_mep_selection (result) {
  $('div.mepFilter').html(result);
  $('#language_selector').on('change', update_language);
  $('#country_selector,#group_selector').on('change', request_mep);
  $('#country_selector,#group_selector').on('change', refine_autocomplete);
  $('#mep_selector').autocomplete({
    source: current_autocomplete_meps
    , select: request_mep
  }).focus(function(){
    $('#mep_selector').autocomplete('search', $(this).val() || ' ');
  });
  $('#refresh_mep').on('click', request_mep);
  $('#language_selector').val(language);
  if (small_group) {
    request_mep();
    $('#country_selector,#group_selector').hide();
  }
}

function refine_autocomplete () {
  var c, g;
  current_autocomplete_meps = [];
  for (var i = 0; i < autocomplete_meps.length; i++) {
    if (((!(c = $('#country_selector').val())) || autocomplete_meps[i].country == c) && (!(g = $('#group_selector').val()) || autocomplete_meps[i].group == g)) {
      current_autocomplete_meps.push(autocomplete_meps[i]);
    }
  }
  $('#mep_selector').autocomplete('option', 'source', current_autocomplete_meps);
}

function reference_message_inputs (result) {
  $('#faxform').html(result);
  $('#name,#hometown,#whycare1,#whycare2,#age').on('change', formulate_message);
  $('#name,#hometown,#whycare1,#whycare2,#age').on('change', showEditor);
  $('#sendfax').on('click', function () {
    // piwik tracking then send
    jQuery.ajax({
        'url': 'https://piwik.netzfreiheit.org/piwik.php?idsite=11&rec=1&url=https%3A%2F%2Fsavetheinternet.eu&idgoal=4&e_c=contact&e_n=fax&e_v=' + (txt_changed ? 1 : 0)
        , 'complete': sendfax
      });
  });
}

/*** 
* AJAX request MEPs 
***/
function request_mep (event, ui) {
  var id = ((ui || {}).item || {}).id || $('#mep_selector').val();
  if ($('#country_selector').val() || small_group) {
    //$.ajax('/sti/choose_mep/', {
    $.ajax('https://faxjh.savetheinternet.eu/sti/choose_mep/', {
      data: {'country': $('#country_selector').val(), 'group': $('#group_selector').val(), 'id': id}
      , success: receive_mep
      , dataType: 'json'
    });  
  } else {
    clear_mep();
  }
}

function clear_mep () {
  mep = null;
  $('#mep_infos_top').html();
  $('#id').val('');
  $('#name,#hometown,#whycare1,#whycare2,#age').hide();
  removeEditor();
}

function receive_mep (data, status, jqXHR) {
  if (data && data.id) {
    mep = data;
    $(get_tmpl('mep_infos')).Chevron('render', data, '#mep_infos_top');   
    $('#id').val(data['id']);
    if (small_group) {
      $('#mep_selector,#refresh_mep,#language_selector').show();
    } else {
      $('#group_selector,#mep_selector,#refresh_mep,#language_selector').show();
    }
    load_user_input();
  } else {
    clear_mep();
  }
}

/***
* handle html-editor ncEditor for main message box
***/ 
function showEditor () {
  if (!editor) {
    $('#full_message').show();
    editor = new nicEditor({buttonList : ['bold','italic','underline','left','center','right','justify','ol','ul','subscript','superscript','strikethrough','removeformat','indent','outdent'], iconsPath: '/static/images/nicEditorIcons.gif'}).panelInstance('full_message').addEvent('blur', function () {
    txt_changed = true;
    });
    $('#sendfax').show();
  }
}

function removeEditor () {
  if (editor) {
    editor.removeInstance('full_message');
    editor = null;
  }
  $('#full_message').hide();
  $('#sendfax').hide();
}

/***
* persist and load user input 
***/
function load_user_input () {
  $('#name,#hometown,#whycare1,#whycare2,#age').show();
  if (typeof window !== 'undefined' && window.localStorage) {
    $('#age').val(window.localStorage.getItem('age'));
    $('#name').val(window.localStorage.getItem('name'));
    $('#hometown').val(window.localStorage.getItem('hometown'));
    if (!$('#whycare1').val()) {
      $('#whycare1').val(window.localStorage.getItem('whycare1-'+language));
    }
    if (!$('#whycare2').val()) {
      $('#whycare2').val(window.localStorage.getItem('whycare2-'+language));
    }
    if ($('#whycare1').val() || $('#whycare2').val()) {
      showEditor();
      formulate_message();
    }
  }
}

function check_and_persist(o, simple) {
  var s;
  if (typeof window !== 'undefined' && window.localStorage) {
    for (var e in o) {
      s = simple ? e : e + '-' + language;
      window.localStorage.setItem(s, o[e]);
    }
  }
}

/***
* formulate full message based on user input and templates
***/
function formulate_message(){
  var args = {'name': trim($('#name').val())
      , 'age': trim($('#age').val())
      , 'hometown': trim($('#hometown').val())};
  if(args.name && args.hometown && args.age) {
    args.has_name_age_hometown = true;
  }
  else if (args.name && args.hometown) {
    args.has_name_hometown = true;
  }
  else if (args.name && args.age) {
    args.has_name_age = true;
  }
  else if (args.name) {
    args.has_name = true;
  }
  else if (args.hometown && args.age) {
    args.has_hometown_age = true;
  } 
  else if (args.hometown) {
    args.has_hometown = true;
  } 
  else if (args.age) {
    args.has_age = true;
  }
  if (args.name || args.age || args.hometown) {
    check_and_persist(args, true);
    $(get_tmpl("intro")).Chevron("render", args, formulate_body);
  } else {
    formulate_body('');
  }
}

function formulate_body (intro) {
  var args = {Introduction: intro
      , whycare1: $('#whycare1').val() || ''
      , whycare2: $('#whycare2').val() || ''
      , age: $('#age').val() || ''
      , Greeting: getMEPName()
      , goodbye: $('#name').val() || 'A concerned citizen'};
  args.haswhycare = args.whycare1 || args.whycare2; 
  check_and_persist({'whycare1': args.whycare1, 'whycare2': args.whycare2});
  $(get_tmpl("message")).Chevron("render", args, render_body);
}

function get_tmpl (tmpl_uri) {
  return '#tmpl_' + language + '_' + tmpl_uri;
}

function render_body (full_message) {;
  nicEditors.findEditor('full_message').setContent(full_message);
}

function getMEPName () {
  if (mep && mep.name) {
    return mep.name;
  }
  return '';
}

function trim(str) {
  return (str || '').replace(/^\s+/,'').replace(/\s+$/,'')
}