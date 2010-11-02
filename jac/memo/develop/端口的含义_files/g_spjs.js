
//验空的函数
function checkblank(id)
{
	ele=document.getElementById(id);
	len=bytes(ele.value);
	if(len==0)
	{
		showerror("msg_blank");
		return false;}
		else
		{	hideerror("msg_blank");
			return true;
			}
	}
//验字节数多于
function checkbytem(id,smax)
{
	ele=document.getElementById(id);
	len=bytes(ele.value);
	if(len>smax)
	{
		showerror("msg_maxthan");
		return false;
		}
		else
		{	hideerror("msg_maxthan");
			return true;
			}
	
	}
//验证字节数少于
function checkbytes(id,smin)
{
	ele=document.getElementById(id);
	len=bytes(ele.value);
	if(len<smin)
	{
		showerror("msg_minthan");
				return false;
		}
		else
		{
		hideerror("msg_minthan");
		return true;}
	}
//验证字节数多于和少于
function checkbyteall(id,smin,smax)
{
	ele=document.getElementById(id);
	len=bytes(ele.value);
	if((len<smin)||(len>smax))
	{
		showerror("msg_than");
				return false;
		}
		else{
		hideerror("msg_than");
		return true;}
	}
//获取字节数目针对中英文和数字
function bytes(str)
{if(typeof(str)!='string'){
		str = str.value;
	}
	var len = 0;
	for(var i = 0; i < str.length; i++){
		if(str.charCodeAt(i) > 127){
			len++;
		}
		len++;
	}
	return len;
	}
//去除左右空格
function trimlr(id)
{
	var str=document.getElementById(id).value;
	for(i=0;str.charAt(i)==" "|| str.charAt(i)=="　";i++)
{
}
str=str.substring(i,str.length);
for(i=str.length-1;str.charAt(i)==" "|| str.charAt(i)=="　";i--)
{
}
str=str.substring(0,i+1);
return str;
	}
//多个空格和换行当做一个使用
function trimrn(id)
{
var el=document.getElementById(id);
var s=el.value;
var len = s.length;
i=0;
flag=0;
flagn=0;
var result="";
while(i<len)
{
	ch=s.charAt(i);
	if(ch=="\n"||ch=="\r")
	{
		if((flagn==1)&&(ch=="\n")){
			flag++;
			flagn=0;
		}else if(ch=="\r"){
			flagn=1;
		}
		
	
			i++;
			if(flag==1)
			{
			result=result+ch;
			}
	
	}else{
		flag=0;
		flagn=0;
		result=result+ch;
		i++;
	}
}
	return result;
}
//统一处理错误问题
function showerror(msg)
{if(msg)
	ob=document.getElementById(msg);
	ob.style.display="block";
	}
function hideerror(msg)
{
	if(msg)
	ob=document.getElementById(msg);
	ob.style.display="none";
}
function setvalue(id)
{
document.getElementById(id).value=trimrn(id);
alert(document.getElementById(id).value);
}
function cutSpace(id)
{
el=document.getElementById(id);
s=el.value;
    var len = s.length;
    var i;
    var ch;
    var result = "";

    i = 0;
    while (i < len)
    {
        ch = s.charAt(i++);
        result += ch;
        if (ch != ' ' && ch !='　')
        {
            continue;
        }

        while (i < len && (ch = s.charAt(i)) == ' ')
        {
           i++;
        }
    }

return result;
}
//从输入项到选中
function getselect(id,selectname)
{

         var ele = document.getElementById(id);

         ele.selectedIndex = selectname;

 

}

