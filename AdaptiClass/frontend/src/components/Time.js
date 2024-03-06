import React, { useEffect, useRef } from 'react';
import styled from 'styled-components';
import Chart from 'chart.js/auto';

const ChartWrapper = styled.div`
  width: 100%;
  padding: 20px 0;
`;

const ChartContainer = styled.div`
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  padding-top: 10px;
  padding-right: 20px;
  padding-bottom: 20px;
  padding-left: 20px;
  width: calc(2 * 317px +10pxS);
  box-sizing: border-box;
`;



const TimeChart = ({ time }) => { 
    const chartRef = useRef(null);
  
    useEffect(() => {
      if (chartRef.current) {
        const ctx = chartRef.current.getContext('2d');
  
        const totalCurrentWeek = time.currentWeek.reduce((acc, cur) => acc + cur.timeSpent, 0);
        const difference = totalCurrentWeek - time.lastWeekTotal;
  
        const maxTimeSpent = Math.max(...time.currentWeek.map(item => item.timeSpent));
        const maxTimeDay = time.currentWeek.find(item => item.timeSpent === maxTimeSpent).day;
  
        const backgroundColors = time.currentWeek.map(item =>
          item.day === maxTimeDay ? 'rgba(255, 159, 64)' : 'rgba(54, 162, 235)'
        );
  
        const myChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: time.currentWeek.map(item => item.day),
            datasets: [{
              label: 'Total Time Spent',
              data: time.currentWeek.map(item => item.timeSpent),
              backgroundColor: backgroundColors,
              borderRadius: 10, 
              borderWidth: 1
            }]
          },
          options: {
            layout: {
              padding: {
                top: 50
              }
            },
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  stepSize: 30,
                  callback: function(value) {
                    return value + ' min';
                  }
                },
                grid: {
                  display: false,
                },
              },
              x: {
                grid: {
                  display: false,
                },
              },
            },
            plugins: {
              legend: {
                display: false,
              },
              title: {
                display: true,
                text: 'Total Time Spent',
                align: 'start',
                font: {
                  size: 18
                }, padding: {
                    top: -40, 
                    bottom: 40  
                  }
              },
              tooltip: {
                enabled: true,
                callbacks: {
                  label: function(context) {
                    return `${context.parsed.y} min`;
                  }
                }
              }
            },
            elements: {
              bar: {
                borderRadius: {
                  topLeft: 10,
                  topRight: 10,
                  bottomLeft: 10,
                  bottomRight: 10
                },
              },
            },
          },
          plugins: [{
            id: 'customText',
            afterDraw: chart => {
              const ctx = chart.ctx;
              const thisWeekHigher = difference >= 0; 
              
              ctx.save();
              ctx.font = 'bold 12px Arial';
              ctx.textAlign = 'left';
          
              const thisWeekX = chart.chartArea.left + 20;
              
              const thisWeekTextWidth = ctx.measureText(`This Week: ${Math.floor(totalCurrentWeek/60)}h ${totalCurrentWeek%60}min`).width;
          
              const gap = 20; 
              const lastWeekX = thisWeekX + thisWeekTextWidth + gap;
          
              const textY = chart.chartArea.bottom + 30; 
          
              ctx.fillStyle = thisWeekHigher ? 'green' : 'red';
              ctx.fillText(`This Week: ${Math.floor(totalCurrentWeek/60)}h ${totalCurrentWeek%60}min`, thisWeekX, textY -260);
              
              ctx.fillStyle = thisWeekHigher ? 'red' : 'green';
              ctx.fillText(`Last Week: ${Math.floor(time.lastWeekTotal/60)}h ${time.lastWeekTotal%60}min`, lastWeekX, textY - 260);
          
              ctx.restore();
            }
          }],
          
          
        });
  
        return () => {
          myChart.destroy();
        };
      }
    }, [time]);
   

 return (
  <ChartWrapper>
    <ChartContainer>
      <canvas id="myChart" ref={chartRef}></canvas>
    </ChartContainer>
  </ChartWrapper>
);

};

export default TimeChart;