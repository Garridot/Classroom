const icon_menu = document.querySelector('#icon_menu')
var menu      = document.querySelector('.menu')
const icon_noti = document.querySelector('#icon-noti')
const noti = document.querySelector('.notifications')
var toggle = 0;
var status = 0; 

function toggleMenu(){
    if(toggle == 0){        
        menu.style.left = '0';   
        icon_noti.disabled = true  
        icon_menu.classList.add('selected')   
        document.querySelector('.content-extends').style.filter= 'blur(1px)'; 
        toggle = 1;  

    } else if(toggle == 1){
        menu.style.left = '-100%';
        icon_noti.disabled = false 
        icon_menu.classList.remove('selected') 
        document.querySelector('.content-extends').style.filter= 'blur(0px)';        
        toggle = 0;    
    } 
}
function toggleNoti(){
    if(status == 0){
        noti.style.visibility = 'visible'
        noti.style.opacity = '1';
        icon_noti.classList.add('selected')
        icon_menu.disabled = true
               
        document.querySelector('.content-extends').style.filter= 'blur(1px)';
        status = 1; 

    } else if(status == 1){
        noti.style.visibility = 'hidden'
        noti.style.opacity = '0';
        icon_noti.classList.remove('selected')
        icon_menu.disabled = false 
        document.querySelector('.content-extends').style.filter= 'blur(0px)';
        status = 0;    
    }
}

icon_noti.addEventListener('click',function(){
    document.querySelector('#alert').style.display = 'none' 
}) 


