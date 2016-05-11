var viewportwidth = 0;
var totalcarouselwidth = 0;



$(document).ready(function(){
	viewportwidth = getviewportwidth();
	enablecarousel(1);
	enablecarousel(2);
	enablecarousel(3);
	enablecarousel('gift');
	enableGalleryTitle();
	enableDeliveryInfoForm();
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

 // *****************************Register*********************************
function enableDeliveryInfoForm(){
	var deliveryBtn = $('#registercontainer submit')
	deliveryBtn.click(function(){
		
	});
}

 // *************************************************************************