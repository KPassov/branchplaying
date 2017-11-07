require 'sinatra'
require 'json'

post '/payload' do
  push = JSON.parse(request.body.read)
  python test.py "I got some JSON: #{push.inspect}"
end

run Sinatra::Application.run!
