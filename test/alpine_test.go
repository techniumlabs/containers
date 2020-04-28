package test

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/docker"
	"github.com/magiconair/properties/assert"
)

func TestAlpineVersion(t *testing.T) {
	tag := "containers/alpine"
	buildOptions := &docker.BuildOptions{
		Tags:      []string{tag},
		BuildArgs: []string{"TIMEZONE=Australia/Sydney", "MAINTAINER=devops@techniumlabs.com"},
	}

	docker.Build(t, "../alpine/3.10", buildOptions)

	opts := &docker.RunOptions{Command: []string{"cat", "/etc/alpine-release"}}
	output := docker.Run(t, tag, opts)
	assert.Equal(t, output, "3.10.4")

	docker.Build(t, "../alpine/3.11", buildOptions)

	opts = &docker.RunOptions{Command: []string{"cat", "/etc/alpine-release"}}
	output = docker.Run(t, tag, opts)
	assert.Equal(t, output, "3.11.5")

}
