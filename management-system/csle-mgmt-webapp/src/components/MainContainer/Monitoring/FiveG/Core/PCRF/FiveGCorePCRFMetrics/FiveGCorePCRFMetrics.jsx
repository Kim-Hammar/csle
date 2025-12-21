import React from 'react'
import './FiveGCorePCRFMetrics.css'
import FiveGCorePCRFVirtualMemoryChart from '../FiveGCorePCRFVirtualMemoryChart/FiveGCorePCRFVirtualMemoryChart.jsx'
import FiveGCorePCRFResidentMemoryChart from '../FiveGCorePCRFResidentMemoryChart/FiveGCorePCRFResidentMemoryChart.jsx'
import FiveGCorePCRFCPUUsageChart from '../FiveGCorePCRFCPUUsageChart/FiveGCorePCRFCPUUsageChart.jsx'
import FiveGCorePCRFOpenFDChart from '../FiveGCorePCRFOpenFDChart/FiveGCorePCRFOpenFDChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G Core metrics for the PCRF service
 */
const FiveGCorePCRFMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGCorePCRFMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGCorePCRFMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">PCRF virtual memory size (bytes)</h3>
              <FiveGCorePCRFVirtualMemoryChart stats={props.fiveGCorePCRFMetrics}
                                               animation={props.animation} animationDuration={props.animationDuration}
                                               animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">PCRF resident memory usage (bytes)</h3>
              <FiveGCorePCRFResidentMemoryChart stats={props.fiveGCorePCRFMetrics}
                                                animation={props.animation} animationDuration={props.animationDuration}
                                                animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">PCRF CPU usage (seconds) </h3>
              <FiveGCorePCRFCPUUsageChart stats={props.fiveGCorePCRFMetrics}
                                          animation={props.animation} animationDuration={props.animationDuration}
                                          animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Number of open file descriptors by PCRF</h3>
              <FiveGCorePCRFOpenFDChart stats={props.fiveGCorePCRFMetrics}
                                        animation={props.animation} animationDuration={props.animationDuration}
                                        animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGCorePCRFMetrics.displayName = 'FiveGCorePCRFMetrics'
FiveGCorePCRFMetrics.propTypes = {}
FiveGCorePCRFMetrics.defaultProps = {}
export default FiveGCorePCRFMetrics
