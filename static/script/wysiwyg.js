(function() {
  $(document).ready(function() {
    var fonts = ['sofia', 'slabo', 'roboto', 'inconsolata', 'ubuntu'];
    var Font = Quill.import('formats/font');
    Font.whitelist = fonts;
    Quill.register(Font, true);


    var fullEditor = new Quill('#quilleditor', {
      modules: {
        'syntax': true,
        'toolbar': [
          [{ 'font': fonts }, { 'size': [] }],
          [ 'bold', 'italic', 'underline', 'strike' ],
          [{ 'color': [] }, { 'background': [] }],
          [{ 'script': 'super' }, { 'script': 'sub' }],
          [{ 'header': '1' }, { 'header': '2' }, 'blockquote', 'code-block' ],
          [{ 'list': 'ordered' }, { 'list': 'bullet'}, { 'indent': '-1' }, { 'indent': '+1' }],
          [ {'direction': 'rtl'}, { 'align': [] }],
          [ 'link', 'image', 'video', 'formula' ],
          [ 'clean' ]
        ],
      },
      theme: 'snow'
    });

    $('.camera').click(function() {
      var index = $(this).index();
      $('#above-container').addClass('demo-active');
      switchEditor(index, editors[index]);
    });

    $('#above-container .prev').click(function() {
      var index = editors.indexOf(window.quill) - 1;
      switchEditor(index, editors[index]);
    });
    $('#above-container .next').click(function() {
      var index = editors.indexOf(window.quill) + 1;
      switchEditor(index, editors[index]);
    });


    $('#demo-container .ql-editor').one('touchstart', function(event) {
      $('#above-container').addClass('demo-active');
      event.preventDefault();
    });

    $('#demo-container .ql-editor').one('focus', function(event) {
      if (!$('#above-container').hasClass('demo-active')) {
        $('#above-container').addClass('demo-active');
      }
    });

    loadFonts();
    $('#carousel-container').animate({ opacity: 1 }, 500);

    console.log("Welcome to Quill!\n\nThe editor on this page is available via `quill`. Give the API a try:\n\n\tquill.formatText(11, 4, 'bold', true);\n\nVisit the API documenation page to learn more: https://quilljs.com/docs/api/\n");
  });

  function loadFonts() {
    window.WebFontConfig = {
      google: { families: [ 'Inconsolata::latin', 'Ubuntu+Mono::latin', 'Slabo+27px::latin', 'Roboto+Slab::latin' ] }
    };
    (function() {
      var wf = document.createElement('script');
      wf.src = 'https://ajax.googleapis.com/ajax/libs/webfont/1/webfont.js';
      wf.type = 'text/javascript';
      wf.async = 'true';
      var s = document.getElementsByTagName('script')[0];
      s.parentNode.insertBefore(wf, s);
    })();
  }

  function switchEditor(i, editor, skip) {
    // Expose as global so people can easily try out the API
    window.quill = editor;
    if (!skip) console.info('window.quill is now bound to', editor);

    $('.camera').removeClass('active');
    $('.camera:eq(' + i + ')').addClass('active');

    $('.prev, .next').css('visibility', 'visible');
    if (i === 0) $('.prev').css('visibility', 'hidden');
    if (i === 2) $('.next').css('visibility', 'hidden');

    $('#carousel-container').css('margin-left', (i*-100) + '%');
  }
})();
