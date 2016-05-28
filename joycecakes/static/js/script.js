var viewportwidth = 0;
var totalcarouselwidth = 0;
var totalpriceforcheckout = 0;
var allimages = $('img');



$(document).ready(function(){
	viewportwidth = getviewportwidth();
	enablecarousel(1);
	enablecarousel(2);
	enablecarousel(3);
	enablecarousel('gift');
	enableGalleryTitle();
	disableUserProfileForm();
	setupAddToCartForm();
	enableimageloadonscroll();
	enableextraimagesclicked();
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

	carouseldiv.scroll(function(){
		enableimageloadonscroll();
	});

	
}



function prevClicked(container){
	viewportwidth = getviewportwidth();		
		var marginleft = parseInt(container.css('margin-left'));
		var marginright = parseInt(container.css('margin-right'));
		var wd = viewportwidth - parseInt($(container).css('width'));

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
		$(this).html('...');
		getCartValsFromAjax($(this).data('urlsubmit')).done(function(value){
			var responsevals = JSON.parse(value);
			num = responsevals.items_length;
			mycartstr = 'My Cart('+num+')';
			$('#id_mycart').html(mycartstr);
			$('#checkoutdiagcartitemslength').html(' '+num);
			var itemid_num = responsevals.item_id;
			$('.item_id_'+itemid_num).html(responsevals.button_text);
		});
	});
}

function removeFromCartInCartHtml(el){
	var urlToSubmit = $(el).data('removecarturl');
	getCartValsFromAjax(urlToSubmit).done(function(){
		window.location.reload();
	});
}


function confirmAllItemPrices(callback){
	var priceurl = $('#cartupdateallprices').data('urlprice');
	getItemPricesJson(priceurl).done(function(value){
		var v = JSON.parse(value);
		var totalprice = 0;
		$('.eachitem').each(function(){
		
		var itemid  = $(this).data('itemid');
		var itemqty = $(this).find('.cartitemqty').val();
		$(this).find('.cartitemsingleprice').html(numberWithCommas(v[itemid]));

		if($.isNumeric(itemqty)){
			var totalsingleprice = itemqty* v[itemid];
			$(this).find('.cartitemtotalprice').html(numberWithCommas(totalsingleprice));
			totalprice = totalprice + totalsingleprice;

		}
	});
		
		$('#cartallitemstotalsaleprice').html(numberWithCommas(totalprice));
		totalpriceforcheckout=totalprice;
		// if(callback){
		// 	callback(totalprice);
		// }
});
}

function getItemPricesJson(priceurl){
	return $.ajax({
		url:priceurl,
	});
}


function getCartValsFromAjax(urlToSubmit){
	return $.ajax({
		url:urlToSubmit,
		success:function(response){
			var responseobj = JSON.parse(response);				
				showcheckoutdialogue();
		// error:function(response){}
		}
	});
}
function showcheckoutdialogue(){

}

function numberWithCommas(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".")+'.0';
}

function visitmyurl(el){
	url = $(el).data('myurl');
	location.href = url;
}
function enableimageloadonscroll(){
	allimages.each(function(){
		if ($(this).visible()){
			var datasrc = $(this).data('src');
			if(datasrc){
				$(this).attr('src',datasrc);
			}
		}
	});	
}


$(document).scroll(function (){
	enableimageloadonscroll();
});

function enableextraimagesclicked(){
	var extraimages = $('.itemdetailextraimages');
	var itemmainimage = $('#itemdetailcontainer img');
	var itemdetailimageprev = $('#itemdetailimageprev');
	var itemdetailimageprevimg = $('#itemdetailimageprev img');
	var wholebody = $('#wholebodydark');
	extraimages.click(function(){
		wholebody.css('display','block');

		var srcval = $(this).find('img').data('src');
		itemdetailimageprevimg.attr('src',srcval);
		itemdetailimageprev.css('display','block');
		itemdetailimageprev.animate({
			opacity:1
		},2000);
		

	});
}

function removeextraimagepopup(){
	var itemdetailimageprev = $('#itemdetailimageprev');
	var wholebody = $('#wholebodydark');

	wholebody.css('display','none');
	itemdetailimageprev.css('display','none');
	itemdetailimageprev.css('opacity',0);


}