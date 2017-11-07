require 'sinatra'
require 'json'

post '/payload' do
  push = JSON.parse(request.body.read)
  system 'python test.py', push.inspect
end

run Sinatra::Application.run!
