import React from 'react'
import './FiveGCorePCFMetrics.css'
import FiveGCorePCFVirtualMemoryChart from '../FiveGCorePCFVirtualMemoryChart/FiveGCorePCFVirtualMemoryChart.jsx'
import FiveGCorePCFResidentMemoryChart from '../FiveGCorePCFResidentMemoryChart/FiveGCorePCFResidentMemoryChart.jsx'
import FiveGCorePCFCPUUsageChart from '../FiveGCorePCFCPUUsageChart/FiveGCorePCFCPUUsageChart.jsx'
import FiveGCorePCFOpenFDChart from '../FiveGCorePCFOpenFDChart/FiveGCorePCFOpenFDChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G Core metrics for the PCF service
 */
const FiveGCorePCFMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGCorePCFMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGCorePCFMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">PCF virtual memory size (bytes)</h3>
              <FiveGCorePCFVirtualMemoryChart stats={props.fiveGCorePCFMetrics}
                                              animation={props.animation} animationDuration={props.animationDuration}
                                              animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">PCF resident memory usage (bytes)</h3>
              <FiveGCorePCFResidentMemoryChart stats={props.fiveGCorePCFMetrics}
                                               animation={props.animation} animationDuration={props.animationDuration}
                                               animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">PCF CPU usage (seconds) </h3>
              <FiveGCorePCFCPUUsageChart stats={props.fiveGCorePCFMetrics}
                                         animation={props.animation} animationDuration={props.animationDuration}
                                         animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Number of open file descriptors by PCF</h3>
              <FiveGCorePCFOpenFDChart stats={props.fiveGCorePCFMetrics}
                                       animation={props.animation} animationDuration={props.animationDuration}
                                       animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGCorePCFMetrics.displayName = 'FiveGCorePCFMetrics'
FiveGCorePCFMetrics.propTypes = {}
FiveGCorePCFMetrics.defaultProps = {}
export default FiveGCorePCFMetrics
