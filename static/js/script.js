const navToggleBtn = document.querySelector("[data-nav-toggle-btn]");
const header = document.querySelector("[data-header]");

navToggleBtn.addEventListener('click',function(){
    header.classList.toggle("active")
})


//dark theme
var dark_icon = document.getElementById('dark-icon');
var selectedTheme = localStorage.getItem("selected-theme");

const getCurrentTheme = () => document.body.classList.contains('dark-theme') ? 'dark': 'light' ;

dark_icon.onclick = function(){
    document.body.classList.toggle('dark-theme');
    localStorage.setItem("selected-theme", getCurrentTheme());

    if(document.body.classList.contains('dark-theme')){
        dark_icon.src = "images/sun.png";
    }
    else{
        dark_icon.src = "images/moon.png";

    }
}

if(selectedTheme){
    document.body.classList[selectedTheme === 'dark' ? 'add': 'remove']('dark-theme');
}
if(selectedTheme == 'dark'){
    dark_icon.src = "images/sun.png";
}
//dark theme end



function registerhandle(){
    console.log('apple11111111111242334234234444s');
    var redirect_register_page = true;
    localStorage.setItem("data", redirect_register_page);

}


// const redirect_register_page = document.querySelector('#register');

// redirect_register_page.addEventListener('click',()=>{

//     setTimeout(myGreeting, 3000);

//     function myGreeting() {

//         console.log('apple');

//     }
 

// });
//login-register end