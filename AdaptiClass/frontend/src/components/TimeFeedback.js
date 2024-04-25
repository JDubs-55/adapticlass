import React, { Component, useEffect, useRef } from 'react';
import styled from 'styled-components';
import Chart from 'chart.js/auto';


const ComponentWrapper = styled.div`
  width: 60%;
  background-color: #fff; 
  border-radius: 10px; 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); 

  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
`;

const ComponentTitle = styled.h5`
  color: #3f434a;
  font-family: 'Poppins';
  font-weight: bold;
  font-size: 24px;
  margin: 0;
  margin-left: 30px;
  margin-top: 30px;
  margin-bottom: 20px;
  align-self: flex-start;
`;

const MainContentWrapper = styled.div`
  width: 100%;
  padding-top: 0;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

`;

const MainContent = styled.div`
  width: 100%;
`;

const ChartWrapper = styled.div`
  max-width: 100%;
  padding: 20px 0;
`;

const ChartContainer = styled.div`
  padding: 20px;
  position: relative;
  box-sizing: border-box;
  margin: auto;
  height: 450px;
  width: 650px;
`;

const CanvasContainer = styled.div`
  height: 350px;
  width: 600px; 
  canvas {
    width: 100% !important; 
    height: 100% !important; 
  }
`;


const Legend = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  bottom: 10px; 
  width: 100%;
`;

const LegendItem = styled.div`
  display: flex;
  align-items: center;
  margin: 0 10px;
`;

const LegendColor = styled.span`
  display: inline-block;
  width: 20px;
  height: 20px;
  background-color: ${(props) => props.color};
  margin-right: 5px;
  border-radius: 2px;
`;

const LegendText = styled.span`
  font-size: 14px;
`;

const TimeFeedback = ({ timeData }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (chartRef.current && timeData) {
      const ctx = chartRef.current.getContext('2d');
      const days = Object.keys(timeData);
      const focusTimes = days.map(day => timeData[day].engaged);
      const notFocusTimes = days.map(day => timeData[day].disengaged);

      const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: days,
          datasets: [
            {
              label: 'Engaged Time',
              data: focusTimes,
              backgroundColor: 'rgba(54, 162, 235)', // Blue
              borderRadius: 10,
            },
            {
              label: 'Disengaged Time',
              data: notFocusTimes,
              backgroundColor: 'rgba(255, 159, 64)', // Orange
              borderRadius: 10,
            }
          ]
        },
        options: {
          maintainAspectRatio: false, 
          responsive: true, 
          scales: {
            x: {
              stacked: true,
              grid: {
                display: false,
              },
            },
            y: {
              stacked: true,
              beginAtZero: true,
              ticks: {
                stepSize: 10,
                callback: function(value) {
                  return value + ' min';
                }
              },
              grid: {
                display: false,
              },
            }
          },
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              enabled: true,
              callbacks: {
                label: function(context) {
                  return `${context.dataset.label}: ${context.parsed.y} min`;
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
      });

      return () => myChart.destroy();
    }
  }, [timeData]);

  return (

    <ComponentWrapper>
      <ComponentTitle>Time Spent on Course</ComponentTitle>
      <MainContentWrapper>
        <MainContent>
          <ChartContainer>
          <CanvasContainer>
            <canvas ref={chartRef}></canvas>
          </CanvasContainer>
          <Legend>
           <LegendItem>
             <LegendColor color="rgba(54, 162, 235)" /> 
             <LegendText>Focused</LegendText>
           </LegendItem>
           <LegendItem>
             <LegendColor color="rgba(255, 159, 64)" /> 
             <LegendText>Unfocused</LegendText>
           </LegendItem>
         </Legend>
         </ChartContainer>
        </MainContent>
      </MainContentWrapper>
    </ComponentWrapper>
    // <ChartWrapper>
    //   <ChartContainer>
    //     <CanvasContainer>
    //       <canvas ref={chartRef}></canvas>
    //     </CanvasContainer>
    //     <Legend>
    //       <LegendItem>
    //         <LegendColor color="rgba(54, 162, 235)" /> 
    //         <LegendText>Focused</LegendText>
    //       </LegendItem>
    //       <LegendItem>
    //         <LegendColor color="rgba(255, 159, 64)" /> 
    //         <LegendText>Unfocused</LegendText>
    //       </LegendItem>
    //     </Legend>
    //   </ChartContainer>
    // </ChartWrapper>
  );
};

export default TimeFeedback;
