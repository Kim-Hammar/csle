import React from 'react'
import './FiveGDURLCMetrics.css'
import FiveGDURLCPDULatencyChart from '../FiveGDURLCPDULatencyChart/FiveGDURLCPDULatencyChart.jsx'
import FiveGDURLCSDULatencyChart from '../FiveGDURLCSDULatencyChart/FiveGDURLCSDULatencyChart.jsx'
import FiveGDURLCPDUErrorsChart from '../FiveGDURLCPDUErrorsChart/FiveGDURLCPDUErrorsChart.jsx'
import FiveGDURLCSDUErrorsChart from '../FiveGDURLCSDUErrorsChart/FiveGDURLCSDUErrorsChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G DU RLC metrics
 */
const FiveGDURLCMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGDULowMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGDULowMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Latency of creating the protocol data unit (PDU) (ns) </h3>
              <FiveGDURLCPDULatencyChart stats={props.fiveGDURLCMetrics}
                                         animation={props.animation} animationDuration={props.animationDuration}
                                         animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Latency of creating the protocol data unit (PDU) (us)</h3>
              <FiveGDURLCSDULatencyChart stats={props.fiveGDURLCMetrics}
                                         animation={props.animation} animationDuration={props.animationDuration}
                                         animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Percentage of lost/malformed protocol data units (PDUs) </h3>
              <FiveGDURLCPDUErrorsChart stats={props.fiveGDURLCMetrics}
                                         animation={props.animation} animationDuration={props.animationDuration}
                                         animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Percentage of dropped/discarded service data units (SDUs)</h3>
              <FiveGDURLCSDUErrorsChart stats={props.fiveGDURLCMetrics}
                                         animation={props.animation} animationDuration={props.animationDuration}
                                         animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGDURLCMetrics.displayName = 'FiveGDURLCMetrics'
FiveGDURLCMetrics.propTypes = {}
FiveGDURLCMetrics.defaultProps = {}
export default FiveGDURLCMetrics
