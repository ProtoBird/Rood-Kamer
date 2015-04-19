(function($, window) {
    $(document).ready(function() {
		  $('#authors').multiselect();
      $('#category').selectize({
          create: true,
          sortField: 'text'
      });
    });
}).call(this, jQuery, window);
