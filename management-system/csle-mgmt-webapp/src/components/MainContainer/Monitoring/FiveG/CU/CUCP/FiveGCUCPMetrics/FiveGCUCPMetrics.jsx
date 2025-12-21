import React from 'react'
import './FiveGCUCPMetrics.css'
import FiveGCUCPRequestsChart from '../FiveGCUCPRequestsChart/FiveGCUCPRequestsChart.jsx'
import FiveGCUCPPDUEventsChart from '../FiveGCUCPPDUEventsChart/FiveGCUCPPDUEventsChart.jsx'
import FiveGCUCPRRCEventsChart from '../FiveGCUCPRRCEventsChart/FiveGCUCPRRCEventsChart.jsx'
import FiveGCUCPReestablishmentEventsChart
  from '../FiveGCUCPReestablishmentEventsChart/FiveGCUCPReestablishmentEventsChart.jsx'
import FiveGCUCPRRCConnectionsChart from '../FiveGCUCPRRCConnectionsChart/FiveGCUCPRRCConnectionsChart.jsx'
import FiveGCUCPHandoversChart from '../FiveGCUCPHandoversChart/FiveGCUCPHandoversChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G CU-CP metrics
 */
const FiveGCUCPMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGCUMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGCUMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Paging and handover events/requests</h3>
              <FiveGCUCPRequestsChart stats={props.fiveGCUMetrics}
                                      animation={props.animation} animationDuration={props.animationDuration}
                                      animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">PDU Session events</h3>
              <FiveGCUCPPDUEventsChart stats={props.fiveGCUMetrics}
                                       animation={props.animation} animationDuration={props.animationDuration}
                                       animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">RRC establishment attempts</h3>
              <FiveGCUCPRRCEventsChart stats={props.fiveGCUMetrics}
                                       animation={props.animation} animationDuration={props.animationDuration}
                                       animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">RRC reestablishment attempts</h3>
              <FiveGCUCPReestablishmentEventsChart stats={props.fiveGCUMetrics}
                                                   animation={props.animation} animationDuration={props.animationDuration}
                                                   animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Number of radio resource control (RRC) connections</h3>
              <FiveGCUCPRRCConnectionsChart stats={props.fiveGCUMetrics}
                                            animation={props.animation} animationDuration={props.animationDuration}
                                            animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Number of handovers</h3>
              <FiveGCUCPHandoversChart stats={props.fiveGCUMetrics}
                                       animation={props.animation} animationDuration={props.animationDuration}
                                       animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGCUCPMetrics.displayName = 'FiveGCUCPMetrics'
FiveGCUCPMetrics.propTypes = {}
FiveGCUCPMetrics.defaultProps = {}
export default FiveGCUCPMetrics
