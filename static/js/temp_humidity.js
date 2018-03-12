function show_temperature_graph(titulo, subtitulo,titulo_yAxis ,
                                xAxis, series) {
    Highcharts.chart('container', {
        chart: {
            type: 'line'
        },
        title: {
            text: titulo
        },
        subtitle: {
            text: subtitulo
        },
        xAxis: xAxis,
        yAxis: {
            title: {
                text: titulo_yAxis
                // text: 'Temperature (°C)'
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: false
            }
        },
        series: series
    });
}

function show_humidity_graph(titulo, subtitulo,
                             xAxis, series) {
    Highcharts.chart('container', {
        chart: {
            type: 'line'
        },
        title: {
            text: titulo
        },
        subtitle: {
            text: subtitulo
        },
        xAxis: xAxis,
        yAxis: {
            title: {
                text: 'Humudity (%)'
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: false
            }
        },
        series: series
    });
}
