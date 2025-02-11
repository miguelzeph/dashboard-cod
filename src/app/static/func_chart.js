function myChart(canvas_name ,title_dataset , x , y, color_bar, title ) {
    
const name = document.getElementById(canvas_name).getContext('2d');
const chart = new Chart(name, {
    type: 'bar',
    data: {
        labels: x,
        datasets: [{
            label: title_dataset,
            data: y,
            borderWidth: 0.25,
            borderColor: 'black',
            backgroundColor: color_bar
        }]
    },
    options: {
        responsive:false,
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Count'
                },
                ticks: {
                    beginAtZero: true
                }                
            }]
        },
        title: {
            display: true,
            text: title
        }
    }
    
})
return chart
};