import React from 'react'
import './FiveGCoreAMFMetrics.css'
import FiveGCoreAMFVirtualMemoryChart from '../FiveGCoreAMFVirtualMemoryChart/FiveGCoreAMFVirtualMemoryChart.jsx'
import FiveGCoreAMFResidentMemoryChart from '../FiveGCoreAMFResidentMemoryChart/FiveGCoreAMFResidentMemoryChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G Core metrics for the AMF service
 */
const FiveGCoreAMFMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGCoreAMFMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGCoreAMFMetrics === null) {
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
              <FiveGCoreAMFVirtualMemoryChart stats={props.fiveGCoreAMFMetrics}
                                              animation={props.animation} animationDuration={props.animationDuration}
                                              animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Central cache size</h3>
              <FiveGCoreAMFResidentMemoryChart stats={props.fiveGCoreAMFMetrics}
                                               animation={props.animation} animationDuration={props.animationDuration}
                                               animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGCoreAMFMetrics.displayName = 'FiveGCUBufferPoolMetrics'
FiveGCoreAMFMetrics.propTypes = {}
FiveGCoreAMFMetrics.defaultProps = {}
export default FiveGCoreAMFMetrics
