
//读取COOKIE
function GetCookieData(sL)
{
    var sRet="";
    var sC=""+document.cookie;
    if(sC.length>0)
    {
        var aC=sC.split(";",100);
        var iC=aC.length;
        for(var i=0;i<iC;i++)
        {
            if(aC[i].indexOf(sL+"=")!=-1)
            {
                var aRet=aC[i].split("=");
                sRet=unescape(aRet[1]);
                break;
            }
        }
    }
    return sRet;
}



//跳转页面显示
function ShowPage(TotalPage,PageIndex,url){
document.write("<table cellspacing=1 class=a2><tr class=a3><td class=a1><b>"+PageIndex+"/"+TotalPage+"</b></td>");
if (PageIndex<6){PageLong=11-PageIndex;}
else
if (TotalPage-PageIndex<6){PageLong=10-(TotalPage-PageIndex)}
else{PageLong=5;}
for (var i=1; i <= TotalPage; i++) {
if (i < PageIndex+PageLong && i > PageIndex-PageLong || i==1 || i==TotalPage){
if (PageIndex==i){document.write("<td>&nbsp;"+ i +"&nbsp;</td>");}else{document.write("<td>&nbsp;<a href=?PageIndex="+i+"&"+url+">"+ i +"</a>&nbsp;</td>");}
}
}
document.write("<td class=a4><input onkeydown=if((event.keyCode==13)&&(this.value!=''))window.location='?PageIndex='+this.value+'&"+url+"'; onkeyup=if(isNaN(this.value))this.value='' style='border:1px solid #698cc3;' size=2></td></tr></table>");
}

//全选复选框
function CheckAll(form){for (var i=0;i<form.elements.length;i++){var e = form.elements[i];if (e.name != 'chkall')e.checked = form.chkall.checked;}}

//全选主题ID复选框
function ThreadIDCheckAll(form){
for (var i=0;i<form.elements.length;i++){
var e = form.elements[i];
if (e.name == 'ThreadID')e.checked = form.chkall.checked;
}
}

//自定义类别
function ChangeCategory()
{
	CategoryName=prompt("请输入类别名称(最多20个字符):","");
	if(!CategoryName) return;
	if(CategoryName.length > 20){alert("类别名称不能大于20个字符！");return false;}
	this.focus();
	i=document.form.Category.length;
	document.form.Category.options[i]=new Option(CategoryName,CategoryName);
	document.form.Category.options[i].selected=true;
}


//菜单
var menuOffX=0	//菜单距连接文字最左端距离
var menuOffY=18	//菜单距连接文字顶端距离

var ie4=document.all&&navigator.userAgent.indexOf("Opera")==-1
var ns6=document.getElementById&&!document.all

function showmenu(e,vmenu,mod){
	which=vmenu
	menuobj=document.getElementById("popmenu")
	menuobj.thestyle=menuobj.style
	menuobj.innerHTML=which
	menuobj.contentwidth=menuobj.offsetWidth
	eventX=e.clientX
	eventY=e.clientY
	var rightedge=document.body.clientWidth-eventX
	var bottomedge=document.body.clientHeight-eventY
	var getlength
		if (rightedge<menuobj.contentwidth){
			getlength=ie4? document.body.scrollLeft+eventX-menuobj.contentwidth+menuOffX : ns6? window.pageXOffset+eventX-menuobj.contentwidth : eventX-menuobj.contentwidth
		}else{
			getlength=ie4? ie_x(event.srcElement)+menuOffX : ns6? window.pageXOffset+eventX : eventX
		}
		menuobj.thestyle.left=getlength+'px'
		if (bottomedge<menuobj.contentheight&&mod!=0){
			getlength=ie4? document.body.scrollTop+eventY-menuobj.contentheight-event.offsetY+menuOffY-23 : ns6? window.pageYOffset+eventY-menuobj.contentheight-10 : eventY-menuobj.contentheight
		}	else{
			getlength=ie4? ie_y(event.srcElement)+menuOffY : ns6? window.pageYOffset+eventY+10 : eventY
		}
	menuobj.thestyle.top=getlength+'px'
	menuobj.thestyle.visibility="visible"
}

function ie_y(e){  
	var t=e.offsetTop;  
	while(e=e.offsetParent){  
		t+=e.offsetTop;  
	}  
	return t;  
}  
function ie_x(e){  
	var l=e.offsetLeft;  
	while(e=e.offsetParent){  
		l+=e.offsetLeft;  
	}  
	return l;  
}  

function highlightmenu(e,state){
	if (document.all)
		source_el=event.srcElement
	else if (document.getElementById)
		source_el=e.target
	if (source_el.className=="menuitems"){
		source_el.id=(state=="on")? "mouseoverstyle" : ""
	}
	else{
		while(source_el.id!="popmenu"){
			source_el=document.getElementById? source_el.parentNode : source_el.parentElement
			if (source_el.className=="menuitems"){
				source_el.id=(state=="on")? "mouseoverstyle" : ""
			}
		}
	}
}

function hidemenu(){if (window.menuobj)menuobj.thestyle.visibility="hidden"}
function dynamichide(e){if ((ie4||ns6)&&!menuobj.contains(e.toElement))hidemenu()}

document.onclick=hidemenu
document.write("<div class=menuskin id=popmenu onmouseover=highlightmenu(event,'on') onmouseout=highlightmenu(event,'off');dynamichide(event)></div>")
// 菜单END

// add area script
function focusEdit(editBox)
{
 if ( editBox.value == editBox.Helptext )
 {
 editBox.value = '';
 editBox.className = 'editbox';
 }
 return true;
}
function blurEdit(editBox)
{
 if ( editBox.value.length == 0 )
 {
 editBox.className = 'editbox Graytitle';
 editBox.value = editBox.Helptext;
 }
}
function ValidateTextboxAdd(box, button)
{
 var buttonCtrl = document.getElementById( button );
 if ( buttonCtrl != null )
 {
 if (box.value == "" || box.value == box.Helptext)
 {
 buttonCtrl.disabled = true;
 }
 else
 {
 buttonCtrl.disabled = false;
 }
 }
}
// add area script end


function loadtree(ino){
frames["hiddenframe"].location.replace("ForumTree.asp?id="+ino+"")
}


function loadThreadFollow(ForumID){
var targetImg =document.getElementById("followImg");
var targetDiv =document.getElementById("follow");
if (targetDiv.style.display!='block'){
frames["hiddenframe"].location.replace("loading.asp?ForumID="+ForumID+"");
targetDiv.style.display="block";
targetImg.src="images/minus.gif";
}else{
targetDiv.style.display="none";
targetImg.src="images/plus.gif";
}
}

function ToggleMenuOnOff (menuName) {
    var menu = document.getElementById(menuName);
    if (menu.style.display == 'none') {
      menu.style.display = 'block';
    } else {
      menu.style.display = 'none';
    }
}

function OpenWindow (target) { 
  window.open(target, "_Child", "toolbar=no,scrollbars=yes,resizable=yes,width=400,height=400"); 
}

function OpenFriendWindow (target) { 
  window.open(target, "Friend", "resizable=yes,resizable=yes,width=320,height=160"); 
}

function log_out()
{
	ht = document.getElementsByTagName("html");
	ht[0].style.filter = "progid:DXImageTransform.Microsoft.BasicImage(grayscale=1)";
	if (confirm('你确定要退出？'))
	{
		return true;
	}
	else
	{
		ht[0].style.filter = "";
		return false;
	}
}