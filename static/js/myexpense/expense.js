let list = document.querySelectorAll('.exsidebar li');


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
            console.log('link milyo ra pasyo')    
            console.log(item)

        }
    
    // else if(window.location.pathname == '/addexpense' ){
    //     let ul = document.querySelectorAll('.exsidebar li') 
    //     let my_expense = ul[4]
    //     my_expense.classList.remove('active');
    //     my_expense.classList.add('active');
    // }  
}
);


//sidebar
let toggle = document.querySelector('.toggle');
let sidebar = document.querySelector('.exsidebar');
let main = document.querySelector('.exmain');

toggle.addEventListener('click',()=>{
    sidebar.classList.toggle('active');
    main.classList.toggle('active');
})

//overview current date

date = new Date();
year = date.getFullYear();
month = date.getMonth() + 1;
day = date.getDate();
document.getElementById("current_date").innerHTML = year+ "-" + month + "-" + day;

// chart js
// const chart = document.querySelector("#myChart").getContext('2d');

// new Chart(chart, {
//     type: 'line',
//     data: {
//       labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Dec'],
//       datasets: [
//         {
//             label: 'APPL',
//             data: [29374,33537,49631,55648,12546,55642,22456,14556,3325,41255,12456,35412],
//             borderColor: 'red',
//             borderWidth: 2,
//         },
//         {
//             label: 'GOGL',
//             data: [26428, 42752, 44861, 38574, 20831, 35973, 21445, 35354, 38246, 48983, 28778, 29544],
//             borderColor: 'blue',
//             borderWidth: 2,
//         },
//         {
//             label: 'TSLA',
//             data: [25441, 30016, 23550, 34735, 22565, 31436, 42067, 24628, 44979, 34537, 47220, 32794],
//             borderColor: 'green',
//             borderWidth: 2,
//         },
//         ]
//     },
//     options: {
//       scales: {
//         y: {
//           beginAtZero: true
//         }
//       }
//     }
//   });


//expand-more====
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
        dark_icon.src = "/static/images/sun.png";
    }
    else{
        dark_icon.src = "/static/images/moon.png";

    }
}

if(selectedTheme){
    document.body.classList[selectedTheme === 'dark' ? 'add': 'remove']('dark-theme');
}
if(selectedTheme == 'dark'){
    dark_icon.src = "/static/images/sun.png";
}
//dark theme end