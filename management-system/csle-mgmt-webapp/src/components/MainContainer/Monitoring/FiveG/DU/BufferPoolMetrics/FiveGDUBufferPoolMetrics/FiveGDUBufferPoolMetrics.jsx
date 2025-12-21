import React from 'react'
import './FiveGDUBufferPoolMetrics.css'
import FiveGDUBufferPoolCacheSizeChart from '../FiveGDUBufferPoolCacheSizeChart/FiveGDUBufferPoolCacheSizeChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G DU app resource usage metrics
 */
const FiveGDUBufferPoolMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGDUBufferPoolMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGDUBufferPoolMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            <div className="col-sm-12 chartsCol">

              <h3 className="chartsTitle">Central cache size</h3>
              <FiveGDUBufferPoolCacheSizeChart stats={props.fiveGDUBufferPoolMetrics}
                                               animation={props.animation} animationDuration={props.animationDuration}
                                               animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGDUBufferPoolMetrics.displayName = 'FiveGDUBufferPoolMetrics'
FiveGDUBufferPoolMetrics.propTypes = {}
FiveGDUBufferPoolMetrics.defaultProps = {}
export default FiveGDUBufferPoolMetrics
