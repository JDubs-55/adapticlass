import React from "react";
import styled from "styled-components";


const BarContainer = styled.div`
  width: 100%;
  border-radius: 5px;
  background-color: red;
  position: relative;
  margin-bottom: 5px;
`;

const BarBackground = styled.div`
  height: 6px;
  border-radius: 5px;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #E8E9EB;
`

const BarFill = styled.div`
  height: 6px;
  border-radius: 5px;
  position: absolute;
  top: 0;
  left: 0;
  width: ${(props) => props.$width || '0%'};
  background-color: #304FFD;
`;


const CompletionBar = ({width}) => {
    return(
        <BarContainer>
            <BarBackground/>
            <BarFill $width={width}/>
        </BarContainer>
    );
};

export default CompletionBar;