require 'json'
require 'logger'
require 'faraday'
require 'uri'
require 'aws-sdk-iotdataplane'

def logger
  @logger ||= Logger.new($stdout, level: Logger::Severity::DEBUG)
end

def auth_azure(tenant_id, client_id, client_secret)
  url = "https://login.microsoftonline.com/#{tenant_id}/oauth2/v2.0/token"
  body = {
    scope: 'https://graph.microsoft.com/.default',
    grant_type: 'client_credentials',
    client_id:,
    client_secret:,
  }
  res = Faraday.post(url) do |req|
    req.headers['Content-Type'] = 'application/x-www-form-urlencoded'
    req.body = URI.encode_www_form(body)
  end

  JSON.parse(res.body)['access_token']
end

def fetch_schedules(access_token, azure_user_principal_name)
  url = "https://graph.microsoft.com/v1.0/users/#{azure_user_principal_name}/calendar/calendarview" 
  res = Faraday.get(url) do |req|
    req.headers['Authorization'] = "Bearer #{access_token}"
    req.headers['Accept'] = 'application/json'
    req.headers['Prefer'] = "outlook.timezone=\"Asia/Tokyo\""
    req.params = {
      startDateTime: (Date.today - 3).to_time.iso8601,
      endDateTime: (Date.today - 2).to_time.iso8601,
      orderby: 'start/dateTime asc'
    }
  end

  JSON.parse(res.body)['value']
end

def print_schedule(schedule)
  logger.debug(schedule)

  started_at = Time.parse(schedule.dig('start', 'dateTime'))
  ended_at = Time.parse(schedule.dig('end', 'dateTime'))
  subject = schedule['type'] == 'exception' ? '非公開' : schedule['subject']
  return unless subject.match?(/Fusic Tech Live/)

  message = { name: subject, started_at: started_at.strftime('%H:%M'), ended_at: ended_at.strftime('%H:%M')}.to_json
  client = Aws::IoTDataPlane::Client.new
  resp = client.publish(topic: "iot-epd-signage/schedules", payload: message)

  logger.debug("published '#{message}'")
end

def lambda_handler(event:, context:)
  logger.debug(event)
  logger.debug(context)

  params = ['AZURE_TENANT_ID', 'AZURE_APP_ID', 'AZURE_APP_SECRET']
  access_token = auth_azure(*params.map { |key| ENV.fetch(key, nil) })
  schedules = fetch_schedules(access_token, ENV.fetch('AZURE_USER_PRINCIPAL_NAME', nil))
  schedules&.each { |schedule| print_schedule(schedule) }
rescue => e
  logger.fatal(e.message)
end
