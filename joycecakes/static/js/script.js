var viewportwidth = 0;
var totalcarouselwidth = 0;



$(document).ready(function(){
	viewportwidth = getviewportwidth();
	enablecarousel(1);
	enablecarousel(2);
	enablecarousel(3);
	enablecarousel('gift');
	enableGalleryTitle();
	disableUserProfileForm();
	setupAddToCartForm();
});

function getviewportwidth(){
	var docwidth = $(document).width();
	if(docwidth > 960){
		return 960;
	}else{
		return docwidth
	}
}

function adjustcontainer(container, estimatedAddedWidth){
	var allitems = container.find('li')
	var totalwidth= 0;
	var allowance = allitems.length * estimatedAddedWidth;
	allitems.each(function (){
		totalwidth = totalwidth + parseInt($(this).css('width'));
	});
	totalwidth = totalwidth + allowance;
	totalcarouselwidth = totalwidth;
	container.css('width',totalwidth);

}

function enablecarousel(num){
	var carouseldiv = $('#carousel'+num);
	var container = carouseldiv.find('.itemscontainer ul');
	adjustcontainer(container,56);
	var prevarrow = carouseldiv.find('.prevarrow');
	var nextarrow = carouseldiv.find('.nextarrow');
	var firstelement = container.find('li:first-child');
	var containerwidth = parseInt(container.css('width'));


	prevarrow.click(function(){
		prevClicked(container);		
	});
	nextarrow.click(function(){
		nextClicked(container);
	});

	
}



function prevClicked(container){
	viewportwidth = getviewportwidth();		
		var marginleft = parseInt(container.css('margin-left'));
		var marginright = parseInt(container.css('margin-right'));
		var wd = viewportwidth - parseInt($(container).css('width'));


		console.log('marginleft ='+marginleft);
		console.log('width = '+wd);
		if(marginleft<=0 && marginleft != wd){
		container.animate({
		marginLeft:"-="+viewportwidth+"px"			
		},500,function(){
			var allowedmargin = gettotalallowedmargin(parseInt($(container).css('width')),viewportwidth);
			if(parseInt(container.css('margin-left'))<(0-allowedmargin)){
				container.animate({
					marginLeft:(0-allowedmargin)
				},100);
			}

		});	
		}	
}
function nextClicked(container){
	viewportwidth = getviewportwidth();
		var marginleft = parseInt(container.css('margin-left'));
		console.log('marginleft = '+marginleft)
		if(marginleft<0){
		container.animate({
			marginLeft:"+="+viewportwidth+"px"			
		},500,function(){
			if(parseInt(container.css('margin-left'))>0){
				container.animate({
					marginLeft:"0px"					
				},100);
			}
		});
		}	
}




function gettotalallowedmargin(totalwidth,viewportwidth){
 	return totalwidth - viewportwidth;
 }

 // *********************************Gallery*******************************
function enableGalleryTitle(){
 	var prevTitleArrow = $('#prevtitlearrow');
 	var nextTitleArrow = $('#nexttitlearrow');
 	var stripContainer = $('#gallerytitlestrip');

 	adjustcontainer(stripContainer,30);

 	prevTitleArrow.click(function(){
 			prevClicked(stripContainer);
 	});
 	nextTitleArrow.click(function(){
 			nextClicked(stripContainer);
 	});

 }

 // ************************************************************************
function disableUserProfileForm(){
	var all_inputs = $('#userprofilecontainer input[type="text"], #userprofilecontainer input[type="email"]');
	var updatebtn = $('#updatebtn');
	var editbtn = $('#editbtn');
	var errorfield = $('.errorlist.nonfield');
	if (errorfield.length<1){
		all_inputs.prop('disabled', true);
		updatebtn.hide();
	}
	else{
		editbtn.hide();
	}
	
	editbtn.click(function (){
		editbtn.fadeOut(500, function(){
			updatebtn.fadeIn(500);
			all_inputs.prop('disabled',false);
		});
	});
}

function setupAddToCartForm(){
	var addToCartBtn = $('.itemaddtocart');
	addToCartBtn.click(function(){
		addItemToCart($(this).data('urlsubmit'));
	});
}

function addItemToCart(urlToSubmit){
	// TODO FINISH THIS
	$.ajax({
		url:urlToSubmit,
		success:function(response){
			var num = $('#id_mycart').data('cartlength');			
			if(response=='added'){
				num+=1
				mycartstr = 'My Cart('+num+')';
				$('#id_mycart').data('cartlength',num);
				$('#id_mycart').html(mycartstr);
				$('#checkoutdiagcartitemslength').html(' '+num);
				showcheckoutdialogue();
			}
			else if(response='available'){

			}
		},
		error:function(){

		}


	});
}
function showcheckoutdialogue(){

}

function checkoutoncartpageclicked(){

}
function continueshoppingcartpageclicked(){

}