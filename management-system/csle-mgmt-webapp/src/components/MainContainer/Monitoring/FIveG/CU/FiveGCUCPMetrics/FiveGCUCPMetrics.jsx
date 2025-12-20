import React from 'react'
import './FiveGCUCPMetrics.css'
import FiveGDULatencyChart from '../../DU/FiveGDULatencyChart/FiveGDULatencyChart.jsx'
import FiveGDUCPUUsageChart from '../../DU/FiveGDUCPUUsageChart/FiveGDUCPUUsageChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G CU-CP metrics
 */
const FiveGCUCPMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGCUMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGCUMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            {/*<div className="col-sm-6 chartsCol">*/}

            {/*  <h3 className="chartsTitle">MAC layer processing latency</h3>*/}
            {/*  <FiveGDULatencyChart stats={props.fiveGCUMetrics}*/}
            {/*                       animation={props.animation} animationDuration={props.animationDuration}*/}
            {/*                       animationDurationFactor={props.animationDurationFactor} />*/}
            {/*</div>*/}
            {/*<div className="col-sm-6 chartsCol">*/}

            {/*  <h3 className="chartsTitle">MAC layer CPU usage %</h3>*/}
            {/*  <FiveGDUCPUUsageChart stats={props.fiveGCUMetrics}*/}
            {/*                       animation={props.animation} animationDuration={props.animationDuration}*/}
            {/*                       animationDurationFactor={props.animationDurationFactor} />*/}
            {/*</div>*/}
          </div>
        </div>
      )
    }
  }
)
FiveGCUCPMetrics.displayName = 'FiveGCUCPMetrics'
FiveGCUCPMetrics.propTypes = {}
FiveGCUCPMetrics.defaultProps = {}
export default FiveGCUCPMetrics
