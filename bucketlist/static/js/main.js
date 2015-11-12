(function(){
	//Add more bucketlists
    var AddMore = {
        originalHtml: '',
        $addForm:  $('#addForm'),
        ShowAddForm: function(){
            AddMore.$addForm.fadeIn();
            AddMore.originalHtml = AddMore.$addMoreBtn.parent().html();
            AddMore.$addMoreBtn.parent().hide().html('<a id="cancelAddMore" href="#">Cancel</a>').fadeIn('slow');
            AddMore.bindEvents('remove');
        },
        HideAddForm: function(){
            AddMore.$addForm.fadeOut();
            AddMore.$cancelAddMoreBtn.parent().hide().html(AddMore.originalHtml).fadeIn('slow');
            AddMore.bindEvents('show');
        },
        init: function(){
            AddMore.$addForm.hide();
            AddMore.bindEvents('show');
        },
        bindEvents: function(action){
            if(action == 'show'){
                $('.close').click();
                AddMore.$addMoreBtn = $('#addMore');
                AddMore.$addMoreBtn.on('click', AddMore.ShowAddForm);
                AddMore.$cancelAddMoreBtn = $('#cancelAddMore'); 
            } else {
                AddMore.$cancelAddMoreBtn = $('#cancelAddMore'); 
                AddMore.$cancelAddMoreBtn.on('click', AddMore.HideAddForm);
                AddMore.$addMoreBtn = $('#addMore');
            }
        }
    }
    AddMore.init();
   
}).call(this);