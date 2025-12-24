import React from 'react'
import './FiveGDUMetrics.css'
import FiveGDULatencyChart from '../FiveGDULatencyChart/FiveGDULatencyChart.jsx'
import FiveGDUCPUUsageChart from '../FiveGDUCPUUsageChart/FiveGDUCPUUsageChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G DU metrics
 */
const FiveGDUMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGDUMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGDUMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">DU MAC layer processing latency</h3>
              <FiveGDULatencyChart stats={props.fiveGDUMetrics}
                                   animation={props.animation} animationDuration={props.animationDuration}
                                   animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">DU MAC layer CPU usage %</h3>
              <FiveGDUCPUUsageChart stats={props.fiveGDUMetrics}
                                   animation={props.animation} animationDuration={props.animationDuration}
                                   animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGDUMetrics.displayName = 'FiveGDUMetrics'
FiveGDUMetrics.propTypes = {}
FiveGDUMetrics.defaultProps = {}
export default FiveGDUMetrics
