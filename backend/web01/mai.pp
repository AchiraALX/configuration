file { '/etc/nginx/sites-available/default':
  ensure => file,
  source => '';
}
