function doupload()
{
	uploading.style.visibility="visible";
}

function columnvisible()
{
	setcolumn.style.visibility="visible";
}

function columnhidden()
{
	setcolumn.style.visibility="hidden";
}


var flag=false;
function DrawImage(ImgD,imgW,imgH){
	var image=new Image();
	image.src=ImgD.src;
	if(image.width>0 && image.height>0){
	flag=true;
	if(image.width/image.height>= imgW/imgH){
	 if(image.width>imgW){
	 ImgD.width=imgW;
	 ImgD.height=(image.height*imgW)/image.width;
	 }else{
	 ImgD.width=image.width;
	 ImgD.height=image.height;
	 }
	 ImgD.alt=image.width+"¡Á"+image.height;
	 }
	else{
	 if(image.height>imgH){
	 ImgD.height=imgH;
	 ImgD.width=(image.width*imgH)/image.height;
	 }else{
	 ImgD.width=image.width;
	 ImgD.height=image.height;
	 }
	 ImgD.alt=image.width+"¡Á"+image.height;
	 }
	}
	/*else{
	ImgD.src="";
	ImgD.alt=""
	}*/
	}


//Êó±ê¹öÂÖ-----------------------------start
var isdrag=false;
function img_zoom(e, o)    //Í¼Æ¬Êó±ê¹öÂÖËõ·Å

{
  var zoom = parseInt(o.style.zoom, 10) || 100;
  zoom += event.wheelDelta / 12;
  if (zoom > 0) o.style.zoom = zoom + '%';
  return false;
}
function mouseover(){
                div1.border="1";
                div1.style.cursor="nw-resize";
}
function mouseout(){
                div1.border="0";        
}
function mousemove(){
        if(isdrag){
                div1.style.width=event.clientX;
                //div1.style.height=event.clientY;
        }
}
function mousedown(){
                div1.setCapture();
                isdrag = true;
                div1.onmousemove=mousemove;
}
function mouseup(){
        div1.releaseCapture();
        isdrag = false;
        //event.returnValue=false;
}
//Êó±ê¹öÂÖ-----------------------------start