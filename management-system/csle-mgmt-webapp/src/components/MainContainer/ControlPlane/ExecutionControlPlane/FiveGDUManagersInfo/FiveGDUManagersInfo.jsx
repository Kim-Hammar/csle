import './FiveGDUManagersInfo.css'
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from '../SpinnerOrButton/SpinnerOrButton.jsx'
import LogsButton from '../LogsButton/LogsButton.jsx'
import {
  FIVE_G_DU_MANAGER_SUBRESOURCE,
  FIVE_G_DU_SUBRESOURCE,
  FIVE_G_UE_SUBRESOURCE,
  START_ALL_PROPERTY,
  STOP_ALL_PROPERTY, DU_MONITOR_SUBRESOURCE
} from '../../../../Common/constants'

/**
 * Subcomponent of the /control-plane page that contains information about 5G DU managers
 */
const FiveGDUManagersInfo = (props) => {
  return (
    <Card className="subCard">
      <Card.Header>
        <Button
          onClick={() => props.setFiveGDUManagersOpen(!props.fiveGDUManagersOpen)}
          aria-controls="fiveGDUManagersBody"
          aria-expanded={props.fiveGDUManagersOpen}
          variant="link"
        >
          <h5 className="semiTitle"> 5G DU managers
            <i className="fa fa-server headerIcon" aria-hidden="true"></i>
          </h5>
        </Button>
      </Card.Header>
      <Collapse in={props.fiveGDUManagersOpen}>
        <div id="fiveGDUManagersOpen" className="cardBodyHidden">
          <div className="aggregateActionsContainer">
            <span className="aggregateActions">Stop all managers:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${FIVE_G_DU_MANAGER_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
              running={true} entity={FIVE_G_DU_MANAGER_SUBRESOURCE}
              name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />
            <span className="aggregateActions">Start all managers:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${FIVE_G_DU_MANAGER_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
              running={false} entity={FIVE_G_DU_MANAGER_SUBRESOURCE}
              name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />

            <span className="aggregateActions">Stop all monitors:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${DU_MONITOR_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
              running={true} entity={DU_MONITOR_SUBRESOURCE}
              name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />
            <span className="aggregateActions">Start all monitors:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${DU_MONITOR_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
              running={false} entity={DU_MONITOR_SUBRESOURCE}
              name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />

            <span className="aggregateActions">Stop all DUs:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${FIVE_G_DU_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
              running={true} entity={FIVE_G_DU_SUBRESOURCE}
              name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />
            <span className="aggregateActions">Start all DUs:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${FIVE_G_DU_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
              running={false} entity={FIVE_G_DU_SUBRESOURCE}
              name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />

            <span className="aggregateActions">Stop all UEs:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${FIVE_G_UE_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
              running={true} entity={FIVE_G_UE_SUBRESOURCE}
              name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />
            <span className="aggregateActions">Start all UEs:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${FIVE_G_UE_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
              running={false} entity={FIVE_G_UE_SUBRESOURCE}
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
                <tr key={`${FIVE_G_DU_MANAGER_SUBRESOURCE}-${index}`}>
                  <td>5G DU manager</td>
                  <td>{props.fiveGDUManagersInfo.ips[index]}</td>
                  <td>{props.fiveGDUManagersInfo.ports[index]}</td>
                  {props.activeStatus(props.fiveGDUManagersInfo.five_g_du_managers_running[index])}
                  <td>
                    <SpinnerOrButton
                      loading={props.loadingEntities.includes(
                        `${FIVE_G_DU_MANAGER_SUBRESOURCE}-`
                        + `${props.fiveGDUManagersInfo.ips[index]}`)}
                      running={props.fiveGDUManagersInfo.five_g_du_managers_running[index]}
                      entity={FIVE_G_DU_MANAGER_SUBRESOURCE} name={FIVE_G_DU_MANAGER_SUBRESOURCE}
                      ip={props.fiveGDUManagersInfo.ips[index]}
                      startOrStop={props.startOrStop}
                    />
                    <LogsButton name={props.fiveGDUManagersInfo.ips[index]}
                                entity={FIVE_G_DU_MANAGER_SUBRESOURCE}
                                getLogs={props.getLogs}
                    />
                  </td>
                </tr>
              )}

              {props.fiveGDUManagersInfo.five_g_du_managers_statuses.map((status, index) =>
                <tr key={`${FIVE_G_DU_SUBRESOURCE}-${index}`}>
                  <td>5G DU</td>
                  <td>{props.fiveGDUManagersInfo.ips[index]}</td>
                  <td></td>
                  {props.activeStatus(status.du_running)}
                  <td>
                    <SpinnerOrButton
                      loading={props.loadingEntities.includes(
                        `${FIVE_G_DU_SUBRESOURCE}-`
                        + `${props.fiveGDUManagersInfo.ips[index]}`)}
                      running={status.du_running}
                      entity={FIVE_G_DU_SUBRESOURCE}
                      name={FIVE_G_DU_SUBRESOURCE}
                      ip={props.fiveGDUManagersInfo.ips[index]}
                      startOrStop={props.startOrStop}
                    />
                    <LogsButton name={props.fiveGDUManagersInfo.ips[index]}
                                entity={FIVE_G_DU_SUBRESOURCE}
                                getLogs={props.getLogs}
                    />
                  </td>
                </tr>
              )}

              {props.fiveGDUManagersInfo.five_g_du_managers_statuses.map((status, index) =>
                <tr key={`${FIVE_G_UE_SUBRESOURCE}-${index}`}>
                  <td>5G UE</td>
                  <td>{props.fiveGDUManagersInfo.ips[index]}</td>
                  <td></td>
                  {props.activeStatus(status.ue_running)}
                  <td>
                    <SpinnerOrButton
                      loading={props.loadingEntities.includes(
                        `${FIVE_G_UE_SUBRESOURCE}-`
                        + `${props.fiveGDUManagersInfo.ips[index]}`)}
                      running={status.ue_running}
                      entity={FIVE_G_UE_SUBRESOURCE}
                      name={FIVE_G_UE_SUBRESOURCE}
                      ip={props.fiveGDUManagersInfo.ips[index]}
                      startOrStop={props.startOrStop}
                    />
                    <LogsButton name={props.fiveGDUManagersInfo.ips[index]}
                                entity={FIVE_G_UE_SUBRESOURCE}
                                getLogs={props.getLogs}
                    />
                  </td>
                </tr>
              )}

              {props.fiveGDUManagersInfo.five_g_du_managers_statuses.map((status, index) =>
                <tr key={`${DU_MONITOR_SUBRESOURCE}-${index}`}>
                  <td>DU monitor thread</td>
                  <td>{props.fiveGDUManagersInfo.ips[index]}</td>
                  <td></td>
                  {props.activeStatus(status.monitor_running)}
                  <td>
                    <SpinnerOrButton
                      loading={props.loadingEntities.includes(
                        `${DU_MONITOR_SUBRESOURCE}-`
                        + `${props.fiveGDUManagersInfo.ips[index]}`)}
                      running={status.monitor_running}
                      entity={DU_MONITOR_SUBRESOURCE}
                      name={DU_MONITOR_SUBRESOURCE}
                      ip={props.fiveGDUManagersInfo.ips[index]}
                      startOrStop={props.startOrStop}
                    />
                    <LogsButton name={props.fiveGDUManagersInfo.ips[index]}
                                entity={DU_MONITOR_SUBRESOURCE}
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
