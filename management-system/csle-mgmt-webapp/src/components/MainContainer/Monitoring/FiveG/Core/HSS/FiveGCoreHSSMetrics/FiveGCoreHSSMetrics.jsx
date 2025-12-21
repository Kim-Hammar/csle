import React from 'react'
import './FiveGCoreHSSMetrics.css'
import FiveGCoreHSSVirtualMemoryChart from '../FiveGCoreHSSVirtualMemoryChart/FiveGCoreHSSVirtualMemoryChart.jsx'
import FiveGCoreHSSResidentMemoryChart from '../FiveGCoreHSSResidentMemoryChart/FiveGCoreHSSResidentMemoryChart.jsx'
import FiveGCoreHSSCPUUsageChart from '../FiveGCoreHSSCPUUsageChart/FiveGCoreHSSCPUUsageChart.jsx'
import FiveGCoreHSSOpenFDChart from '../FiveGCoreHSSOpenFDChart/FiveGCoreHSSOpenFDChart.jsx'
import FiveGCoreHSSRegistrationEventsChart
  from '../FiveGCoreHSSRegistrationEventsChart/FiveGCoreHSSRegistrationEventsChart.jsx'
import FiveGCoreHSSAuthenticationEventsChart
  from '../FiveGCoreHSSAuthenticationEventsChart/FiveGCoreHSSAuthenticationEventsChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G Core metrics for the HSS service
 */
const FiveGCoreHSSMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGCoreHSSMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGCoreHSSMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Virtual memory size (bytes)</h3>
              <FiveGCoreHSSVirtualMemoryChart stats={props.fiveGCoreHSSMetrics}
                                              animation={props.animation} animationDuration={props.animationDuration}
                                              animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Resident memory usage (bytes)</h3>
              <FiveGCoreHSSResidentMemoryChart stats={props.fiveGCoreHSSMetrics}
                                               animation={props.animation} animationDuration={props.animationDuration}
                                               animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">CPU usage (seconds) </h3>
              <FiveGCoreHSSCPUUsageChart stats={props.fiveGCoreHSSMetrics}
                                         animation={props.animation} animationDuration={props.animationDuration}
                                         animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Number of open file descriptors</h3>
              <FiveGCoreHSSOpenFDChart stats={props.fiveGCoreHSSMetrics}
                                       animation={props.animation} animationDuration={props.animationDuration}
                                       animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Number of HSS registrations </h3>
              <FiveGCoreHSSRegistrationEventsChart stats={props.fiveGCoreHSSMetrics}
                                                   animation={props.animation} animationDuration={props.animationDuration}
                                                   animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Number of HSS authentications </h3>
              <FiveGCoreHSSAuthenticationEventsChart stats={props.fiveGCoreHSSMetrics}
                                                   animation={props.animation} animationDuration={props.animationDuration}
                                                   animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGCoreHSSMetrics.displayName = 'FiveGCoreHSSMetrics'
FiveGCoreHSSMetrics.propTypes = {}
FiveGCoreHSSMetrics.defaultProps = {}
export default FiveGCoreHSSMetrics
