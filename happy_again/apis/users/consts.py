from happy_again.common.consts import deployment

USER_ALREADY_REGISTERED = "User '{}' -> already registered or tasks not completed"
TASK_NOT_COMPLETED = "User '{}' -> tasks not completed"
USER_NOT_REGISTERED = "User '{}' -> not registered"
EMAIL_IS_REQUIRED = "Email is required"

if deployment:
  CONFIRMATION_URL = "{site}/register/success/{token}" #DEPLOYED
else:
  CONFIRMATION_URL = "http://localhost:4200/register/success/{token}" #LOCAL

if deployment:
  RESET_PASSWORD_URL = "{site}/reset-password/{token}" #DEPLOYED
else:
  RESET_PASSWORD_URL = "http://localhost:4200/reset-password/{token}" #LOCAL

USER_REGISTERED = "User '{}' -> registered"
TOKEN_EXPIRED = "Token expired"
USER_RESET_PASSWORD_LINK_SENT = "User password reset link has been sent"
INVALID_TOKEN = "Invalid token"
INVALID_USER = "Invalid user"
INVALID_PASSWORD = "Invalid password"
ALREADY_CONFIRMED = "User already confirmed"
USER_CONFIRMED = "User confirmed"
EMAIL_NOT_CONFIRMED = "Email not confirmed"
USER_LOGGED_IN = "User logged in successfully"
USER_LOGGED_OFF = "User logged off successfully"
INVALID_SESSION = "Invalid session"
INVALID_USER_INFO = "invalid user info"
SESSION_INFORMATION_UPDATED = "Session information updated"
USER_ALREADY_LOGGED_OFF = "User already logged off"
USER_PASSWORD_RESET = "Password of the user has been reset"
USER_BLOCKED = "User blocked"
USER_UNBLOCKED = "User unblocked"
EXTEND_TIME = "User time extended"
INCOMPLETE_BODY_PARAMETER = "One or more parameter missing"


SUBJECT_USER_CONFIRMATION_EMAIL = '{lan[40]}'
SUBJECT_USER_RESET_PASSWORD = '{lan[41]}'

HTML_MESSAGE_REGISTER = """
    <!--INFORMATION SHEET-->
    <div style="text-align: justify;">
      <h1>{lan[0]}</h1>
      <h4 style="margin-bottom: 0px">{lan[1]}</h4>
      <p style="margin-top: 2px">
        {lan[14]}
      </p>
      <h4 style="margin-bottom: 0px">{lan[2]}</h4>
      <p style="margin-top: 2px">
      {lan[15]}
      </p>
      <h4 style="margin-bottom: 0px">{lan[3]}</h4>
      <p style="margin-top: 2px">
        {lan[16]}
      </p>
      <h4 style="margin-bottom: 0px">{lan[4]}</h4>
      <p style="margin-top: 2px">
        {lan[17]}
      </p>
      <h4 style="margin-bottom: 0px">{lan[5]}</h4>
      <ul>
        <li>
          {lan[18]}
        </li>
        <li>
          {lan[19]}
        </li>
        <li>
          {lan[20]}
        </li>
        <li>
          {lan[21]}
        </li>
        <li>
          {lan[22]}
        </li>
        <li>
          {lan[23]}
        </li>
        <li>
          {lan[24]}
        </li>
        <li>
          {lan[25]}
        </li>
        <li>
          {lan[26]}
        </li>
      </ul>
      <h4 style="margin-bottom: 0px">{lan[6]}</h4>
      <p style="margin-top: 2px">
        {lan[27]}
      </p>
      <h4 style="margin-bottom: 0px">{lan[7]}</h4>
      <p style="margin-top: 2px">
        {lan[28]}
      </p>
      <h4>{lan[8]}</h4>
      <h4 style="margin-bottom: 0px; text-decoration: underline;">{lan[9]}</h4>
      <p style="margin-top: 2px">
        Dr Helge Gillmeister (email: helge@essex.ac.uk) <br />
        Dr Loes van Dam (email: lvandam@essex.ac.uk) <br />
        Dr Caterina Cinel (email: ccinel@essex.ac.uk) <br />
        Dr Vito de Feo (email: vito.defeo@essex.ac.uk)
      </p>
      <h4 style="margin-bottom: 0px; text-decoration: underline;">{lan[10]}</h4>
      <p style="margin-top: 2px">
        Prof Sheina Orbell (sorbell@essex.ac.uk)
      </p>
      <h4 style="margin-bottom: 0px; text-decoration: underline;">
        {lan[11]}
      </h4>
      <p style="margin-top: 2px">
        Sarah Manning-Press, Research & Enterprise Office, University of Essex, Wivenhoe Park, CO4 3SQ, Colchester.
        Email: sarahm@essex.ac.uk. Phone: 01206-873561
      </p>
    </div>

    <!--CONSENT FORM-->
    <div>
      <h1>{lan[12]}</h1>
      <ol type="1">
        <li>{lan[29]} </li>

        <li>{lan[30]}</li>

        <li>{lan[31]}</li>

        <li>{lan[32]}</li>

        <li>{lan[33]}</li>

        <li>{lan[34]}</li>

        <li>{lan[35]}</li>
        <li>{lan[36]}</li>
      </ol>

      <input type="checkbox" checked disabled> {lan[42]}

      <h1>{lan[13]}</h1>
      <p><b>{lan[37]}</b></p><a href='{url}'>{url}</a>
    </div>
"""
HTML_MESSAGE_RESET_PASSWORD = """
<h1>{lan[38]}</h1>
    <p><b>{lan[39]}</b></p><a href='{url}'>{url}</a>
"""

