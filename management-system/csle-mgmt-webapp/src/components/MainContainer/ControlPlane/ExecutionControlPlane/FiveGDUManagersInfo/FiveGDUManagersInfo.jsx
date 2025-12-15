import './FiveGDUManagersInfo.css'
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from '../SpinnerOrButton/SpinnerOrButton.jsx'
import LogsButton from '../LogsButton/LogsButton.jsx'
import {
  HOST_MONITOR_SUBRESOURCE,
  HOST_MANAGER_SUBRESOURCE,
  START_ALL_PROPERTY,
  STOP_ALL_PROPERTY, FILEBEAT_SUBRESOURCE, PACKETBEAT_SUBRESOURCE, METRICBEAT_SUBRESOURCE,
  HEARTBEAT_SUBRESOURCE
} from '../../../../Common/constants'

/**
 * Subcomponent of the /control-plane page that contains information about 5G DU managers
 */
const FiveGDUManagersInfo = (props) => {
  console.log(props.fiveGDUManagersOpen)
  return (
    <Card className="subCard">
      <Card.Header>
        <Button
          onClick={() => props.setFiveGDUManagersOpen(!props.fiveGDUManagersOpen)}
          aria-controls="hostManagersBody"
          aria-expanded={props.fiveGDUManagersOpen}
          variant="link"
        >
          <h5 className="semiTitle"> 5G DU managers
            <i className="fa fa-server headerIcon" aria-hidden="true"></i>
          </h5>
        </Button>
      </Card.Header>
      <Collapse in={props.fiveGDUManagersOpen}>
        <div id="hostManagersOpen" className="cardBodyHidden">
          <div className="aggregateActionsContainer">
            <span className="aggregateActions">Stop all managers:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${HOST_MANAGER_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
              running={true} entity={HOST_MANAGER_SUBRESOURCE}
              name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />
            <span className="aggregateActions">Start all managers:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${HOST_MANAGER_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
              running={false} entity={HOST_MANAGER_SUBRESOURCE}
              name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />
          </div>

          <div className="table-responsive">
            <Table striped bordered hover>
              <thead>
              <tr>
                <th>Service</th>
                <th>IP</th>
                <th>Port</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
              </thead>
              <tbody>
              {props.fiveGDUManagersInfo.five_g_du_managers_statuses.map((status, index) =>
                <tr key={`${HOST_MANAGER_SUBRESOURCE}-${index}`}>
                  <td>5G DU manager</td>
                  <td>{props.fiveGDUManagersInfo.ips[index]}</td>
                  <td>{props.fiveGDUManagersInfo.ports[index]}</td>
                  {props.activeStatus(props.fiveGDUManagersInfo.five_g_du_managers_running[index])}
                  <td>
                    <SpinnerOrButton
                      loading={props.loadingEntities.includes(
                        `${HOST_MANAGER_SUBRESOURCE}-`
                        + `${props.fiveGDUManagersInfo.ips[index]}`)}
                      running={props.fiveGDUManagersInfo.five_g_du_managers_running[index]}
                      entity={HOST_MANAGER_SUBRESOURCE} name={HOST_MANAGER_SUBRESOURCE}
                      ip={props.fiveGDUManagersInfo.ips[index]}
                      startOrStop={props.startOrStop}
                    />
                    <LogsButton name={props.fiveGDUManagersInfo.ips[index]}
                                entity={HOST_MANAGER_SUBRESOURCE}
                                getLogs={props.getLogs}
                    />
                  </td>
                </tr>
              )}
              </tbody>
            </Table>
          </div>
        </div>
      </Collapse>
    </Card>
  )

}

FiveGDUManagersInfo.propTypes = {}
FiveGDUManagersInfo.defaultProps = {}
export default FiveGDUManagersInfo
