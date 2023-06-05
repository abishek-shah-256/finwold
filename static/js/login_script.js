//login-register
const sign_up_btn = document.querySelector('#sign-up-btn');
const sign_in_btn = document.querySelector('#sign-in-btn');

const login_container = document.querySelector('.login-container');

sign_up_btn.addEventListener('click',()=>{
    login_container.classList.add("sign-up-mode");
    login_container.classList.remove("sign-in-mode");
});

sign_in_btn.addEventListener('click',()=>{
    login_container.classList.add("sign-in-mode");
    login_container.classList.remove("sign-up-mode");

});
//login-register js ends


function registerhandle(){
    // console.log('appleeeeeee');
    var redirect_register_page = true;
    localStorage.setItem("data", redirect_register_page);
    
}

//showing data from index's register navbar to show register animation
var redirect_register_page = localStorage.getItem("data");
console.log('aarko page ma aayo-> ' + redirect_register_page)

// setTimeout(slide_to_register, 0);
//self_execution function->
var slide_to_register = function(){

    var redirect_register_page = localStorage.getItem("data");

    if (redirect_register_page == 'true'){
        login_container.classList.add("sign-up-mode");
        login_container.classList.remove("sign-in-mode");

        var redirect_register_page = false;
        localStorage.setItem("data", redirect_register_page);
    }
    else if (redirect_register_page == 'false'){
        login_container.classList.add("sign-in-mode");
        login_container.classList.remove("sign-up-mode");
        var redirect_register_page = true;
        localStorage.setItem("data", redirect_register_page);
    }


    if (window.location.pathname == '/login_page'){
        login_container.classList.add("sign-in-mode");
        login_container.classList.remove("sign-up-mode");
    }
    else if (window.location.pathname == '/register_page'){
        login_container.classList.add("sign-up-mode");
        login_container.classList.remove("sign-in-mode");
    }

}(); //self_execution