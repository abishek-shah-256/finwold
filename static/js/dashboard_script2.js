let list = document.querySelectorAll('.sidebar li');


// ==========FOR SELECTOR IN SINGLE PAGE WEBPAGE=========
// function activeLink(){
//     list.forEach((item)=>
//     item.classList.remove('active'));
//     this.classList.add('active');
// }

// list.forEach((item) =>
// item.addEventListener('click',activeLink));

// ==========FOR SELECTOR IN DIFFEREnt PAGE WEBPAGE=========
list.forEach((item)=>{
    // console.log(item)
    // console.log(item.firstElementChild.getAttribute('href') , window.location.pathname)
    // console.log(item.firstElementChild.href , window.location.href)

    if( item.firstElementChild.getAttribute('href') === window.location.pathname){
            item.classList.remove('active');
            item.classList.add('active');
            // console.log('link milyo ra pasyo')    
        }
}
);


//sidebar
let toggle = document.querySelector('.toggle');
let sidebar = document.querySelector('.sidebar');
let main = document.querySelector('.main');

toggle.addEventListener('click',()=>{
    sidebar.classList.toggle('active');
    main.classList.toggle('active');
})

//overview current date

date = new Date();
year = date.getFullYear();
month = date.getMonth() + 1;
day = date.getDate();
document.getElementById("current_date").innerHTML = month + "/" + day + "/" + year;

//====expand-more-btn====
let expand_more = document.querySelector('.expand-more');
let expand_more_items = document.querySelector('.expand-more-items');

expand_more.addEventListener('click',()=>{
    expand_more_items.classList.toggle('active');
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