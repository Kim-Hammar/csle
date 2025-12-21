import React from 'react'
import './FiveGCoreUPFMetrics.css'
import FiveGCoreUPFVirtualMemoryChart from '../FiveGCoreUPFVirtualMemoryChart/FiveGCoreUPFVirtualMemoryChart.jsx'
import FiveGCoreUPFResidentMemoryChart from '../FiveGCoreUPFResidentMemoryChart/FiveGCoreUPFResidentMemoryChart.jsx'
import FiveGCoreUPFCPUUsageChart from '../FiveGCoreUPFCPUUsageChart/FiveGCoreUPFCPUUsageChart.jsx'
import FiveGCoreUPFOpenFDChart from '../FiveGCoreUPFOpenFDChart/FiveGCoreUPFOpenFDChart.jsx'
import FiveGCoreUPFSessionsChart from '../FiveGCoreUPFSessionsChart/FiveGCoreUPFSessionsChart.jsx'
import FiveGCoreUPFGTPPacketsChart from '../FiveGCoreUPFGTPPacketsChart/FiveGCoreGTPPacketsChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G Core metrics for the UPF service
 */
const FiveGCoreUPFMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGCoreUPFMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGCoreUPFMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">UPF virtual memory size (bytes)</h3>
              <FiveGCoreUPFVirtualMemoryChart stats={props.fiveGCoreUPFMetrics}
                                              animation={props.animation} animationDuration={props.animationDuration}
                                              animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">UPF resident memory usage (bytes)</h3>
              <FiveGCoreUPFResidentMemoryChart stats={props.fiveGCoreUPFMetrics}
                                               animation={props.animation} animationDuration={props.animationDuration}
                                               animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">UPF CPU usage (seconds) </h3>
              <FiveGCoreUPFCPUUsageChart stats={props.fiveGCoreUPFMetrics}
                                         animation={props.animation} animationDuration={props.animationDuration}
                                         animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Number of open file descriptors by UPF</h3>
              <FiveGCoreUPFOpenFDChart stats={props.fiveGCoreUPFMetrics}
                                       animation={props.animation} animationDuration={props.animationDuration}
                                       animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>

          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">UPF Sessions </h3>
              <FiveGCoreUPFSessionsChart stats={props.fiveGCoreUPFMetrics}
                                         animation={props.animation} animationDuration={props.animationDuration}
                                         animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Packets on the N3 interface </h3>
              <FiveGCoreUPFGTPPacketsChart stats={props.fiveGCoreUPFMetrics}
                                           animation={props.animation} animationDuration={props.animationDuration}
                                           animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGCoreUPFMetrics.displayName = 'FiveGCoreUPFMetrics'
FiveGCoreUPFMetrics.propTypes = {}
FiveGCoreUPFMetrics.defaultProps = {}
export default FiveGCoreUPFMetrics
