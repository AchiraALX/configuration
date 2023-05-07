file { '/etc/haproxy/haproxy.cfg':
  ensure => file,
  source => '/home/ubuntu/configuration/load_balancer/config.cfg';
}
