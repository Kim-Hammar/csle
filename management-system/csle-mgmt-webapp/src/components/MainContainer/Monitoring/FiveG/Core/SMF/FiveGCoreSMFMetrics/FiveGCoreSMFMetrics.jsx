import React from 'react'
import './FiveGCoreSMFMetrics.css'
import FiveGCoreSMFVirtualMemoryChart from '../FiveGCoreSMFVirtualMemoryChart/FiveGCoreSMFVirtualMemoryChart.jsx'
import FiveGCoreSMFResidentMemoryChart from '../FiveGCoreSMFResidentMemoryChart/FiveGCoreSMFResidentMemoryChart.jsx'
import FiveGCoreSMFCPUUsageChart from '../FiveGCoreSMFCPUUsageChart/FiveGCoreSMFCPUUsageChart.jsx'
import FiveGCoreSMFOpenFDChart from '../FiveGCoreSMFOpenFDChart/FiveGCoreSMFOpenFDChart.jsx'
import FiveGCoreSMFSessionsChart from '../FiveGCoreSMFSessionsChart/FiveGCoreSMFSessionsChart.jsx'
import FiveGCoreSMFPeersChart from '../FiveGCoreSMFPeersChart/FiveGCoreSMFPeersChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G Core metrics for the SMF service
 */
const FiveGCoreSMFMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGCoreSMFMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGCoreSMFMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">SMF virtual memory size (bytes)</h3>
              <FiveGCoreSMFVirtualMemoryChart stats={props.fiveGCoreSMFMetrics}
                                              animation={props.animation} animationDuration={props.animationDuration}
                                              animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">SMF resident memory usage (bytes)</h3>
              <FiveGCoreSMFResidentMemoryChart stats={props.fiveGCoreSMFMetrics}
                                               animation={props.animation} animationDuration={props.animationDuration}
                                               animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">SMF CPU usage (seconds) </h3>
              <FiveGCoreSMFCPUUsageChart stats={props.fiveGCoreSMFMetrics}
                                         animation={props.animation} animationDuration={props.animationDuration}
                                         animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Number of open file descriptors by SMF</h3>
              <FiveGCoreSMFOpenFDChart stats={props.fiveGCoreSMFMetrics}
                                       animation={props.animation} animationDuration={props.animationDuration}
                                       animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>

          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">SMF Sessions </h3>
              <FiveGCoreSMFSessionsChart stats={props.fiveGCoreSMFMetrics}
                                         animation={props.animation} animationDuration={props.animationDuration}
                                         animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">SMF Peers</h3>
              <FiveGCoreSMFPeersChart stats={props.fiveGCoreSMFMetrics}
                                      animation={props.animation} animationDuration={props.animationDuration}
                                      animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGCoreSMFMetrics.displayName = 'FiveGCoreSMFMetrics'
FiveGCoreSMFMetrics.propTypes = {}
FiveGCoreSMFMetrics.defaultProps = {}
export default FiveGCoreSMFMetrics
