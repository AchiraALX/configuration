file { '/etc/nginx/sites-available/default':
  ensure => file,
  source => '/home/ubuntu/configuration/backend/default',
}
