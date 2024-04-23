import React, { useEffect, useRef } from 'react';
import styled from 'styled-components';
import Chart from 'chart.js/auto';

const ChartWrapper = styled.div`
  width: 100%;
  height: 50%;
`;

const ChartContainer = styled.div`
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  padding: 20px;
  width: calc(2 * 317px +10px);
  box-sizing: border-box;
  max-height: 400px;
`;



const TimeChart = ({ time, total_time, total_time_prev_week }) => { 
    const chartRef = useRef(null);
  
    useEffect(() => {
      if (chartRef.current && time && total_time && total_time_prev_week) {
        const ctx = chartRef.current.getContext('2d');
  
        const totalCurrentWeek = total_time;
        const difference = total_time - total_time_prev_week;
  
        const maxTimeSpent = Math.max(...time.map(item => item.time_spent));
        const maxTimeDay = time.find(item => item.time_spent === maxTimeSpent).day;
  
        const backgroundColors = time.map(item =>
          item.day === maxTimeDay ? '#FF965D' : '#304FFD'
        );
  
        const myChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: time.map(item => item.day),
            datasets: [{
              label: 'Total Time Spent',
              data: time.map(item => item.time_spent),
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
                  family: 'Poppins',
                  size: 24,
                  weight: 'bold',
                }, 
                padding: {
                    top: -40, 
                    bottom: 20  
                },
                color: '#3f434a'
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
              ctx.font = 'bold 15px Poppins';
              ctx.textAlign = 'left';

              const chartArea = chart.chartArea;
              const chartWidth = chartArea.right - chartArea.left;
              const chartHeight = chartArea.bottom - chartArea.top;

              const thisWeekText = `This Week: ${Math.floor(totalCurrentWeek/60)}h ${totalCurrentWeek%60}min`;
              const lastWeekText = `Last Week: ${Math.floor(total_time_prev_week/60)}h ${total_time_prev_week%60}min`;
              
              const thisWeekTextWidth = ctx.measureText(thisWeekText).width;
              const lastWeekTextWidth = ctx.measureText(lastWeekText).width;

              const gap = 20; 
              const totalTextWidth = thisWeekTextWidth + lastWeekTextWidth + gap;
              
              const textX = (chartWidth - totalTextWidth);

              const textY = chartArea.top - 28;

          
              ctx.fillStyle = thisWeekHigher ? '#49C96D' : '#FD7972';
              ctx.fillText(thisWeekText, textX, textY);
              
              ctx.fillStyle = '#3f434a';
              ctx.fillText(lastWeekText, textX + thisWeekTextWidth + gap, textY);

              ctx.restore();
          
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