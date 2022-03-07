import {Tabulator} from 'https://unpkg.com/tabulator-tables@/dist/js/tabulator_esm.min.js';



let table = new Tabulator("#chart-table", {
    layout:"fitColumns",
    height:"311px",
    columns:[
    {title:"Name", field:"name"},
    {title:"Progress", field:"progress", hozAlign:"right", sorter:"number"},
    {title:"Gender", field:"gender"},
    {title:"Rating", field:"rating", hozAlign:"center"},
    {title:"Favourite Color", field:"col"},
    ],
})

table.setData([
    {id:1,name:"Billy Bob", progress:"12", gender:"male", rating:1, col:"red"} 
])
    