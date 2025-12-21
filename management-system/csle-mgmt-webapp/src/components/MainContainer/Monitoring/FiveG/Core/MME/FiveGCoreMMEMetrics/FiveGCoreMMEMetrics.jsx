import React from 'react'
import './FiveGCoreMMEMetrics.css'
import FiveGCoreMMEVirtualMemoryChart from '../FiveGCoreMMEVirtualMemoryChart/FiveGCoreMMEVirtualMemoryChart.jsx'
import FiveGCoreMMEResidentMemoryChart from '../FiveGCoreMMEResidentMemoryChart/FiveGCoreMMEResidentMemoryChart.jsx'
import FiveGCoreMMECPUUsageChart from '../FiveGCoreMMECPUUsageChart/FiveGCoreMMECPUUsageChart.jsx'
import FiveGCoreMMEOpenFDChart from '../FiveGCoreMMEOpenFDChart/FiveGCoreMMEOpenFDChart.jsx'
import FiveGCoreMMESessionsChart from '../FiveGCoreMMESessionsChart/FiveGCoreMMESessionsChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G Core metrics for the MME service
 */
const FiveGCoreMMEMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGCoreMMEMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGCoreMMEMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">MME virtual memory size (bytes)</h3>
              <FiveGCoreMMEVirtualMemoryChart stats={props.fiveGCoreMMEMetrics}
                                              animation={props.animation} animationDuration={props.animationDuration}
                                              animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">MME resident memory usage (bytes)</h3>
              <FiveGCoreMMEResidentMemoryChart stats={props.fiveGCoreMMEMetrics}
                                               animation={props.animation} animationDuration={props.animationDuration}
                                               animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">MME CPU usage (seconds) </h3>
              <FiveGCoreMMECPUUsageChart stats={props.fiveGCoreMMEMetrics}
                                         animation={props.animation} animationDuration={props.animationDuration}
                                         animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Number of open file descriptors by MME</h3>
              <FiveGCoreMMEOpenFDChart stats={props.fiveGCoreMMEMetrics}
                                       animation={props.animation} animationDuration={props.animationDuration}
                                       animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-12 chartsCol">

              <h3 className="chartsTitle">MME sessions</h3>
              <FiveGCoreMMESessionsChart stats={props.fiveGCoreMMEMetrics}
                                         animation={props.animation} animationDuration={props.animationDuration}
                                         animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGCoreMMEMetrics.displayName = 'FiveGCoreMMEMetrics'
FiveGCoreMMEMetrics.propTypes = {}
FiveGCoreMMEMetrics.defaultProps = {}
export default FiveGCoreMMEMetrics
